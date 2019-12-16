# 正式版

import pandas as pd
from pyecharts.chart import Chart
from pyecharts.option import get_all_options


def values2keys(dict):
    """取出任意字典中所有值升序排序后对应的所有键的列表形式"""

    temp_list = []
    temp_dict = {}
    for k, v in dict.items():
        temp_dict.setdefault(v, []).append(k)

    for i in sorted(list(temp_dict.keys())):
        for j in temp_dict[i]:
            temp_list.append(j)
    return temp_list


class Bar(Chart):
    """
    <<< 动态 柱状图/条形图 >>>
    柱状/条形图，通过柱形的高度/条形的宽度来表现数据的大小。
    """

    def __init__(self, title="", subtitle="", **kwargs):
        super(Bar, self).__init__(title, subtitle, **kwargs)

    def add(self, *args, **kwargs):
        self.__add(*args, **kwargs)

    def __add(self, name, x_axis, y_axis, is_stack=False, bar_category_gap="20%", **kwargs):
        """
        :param name:
            系列名称，用于 tooltip 的显示，legend 的图例筛选。
        :param x_axis:
            x 坐标轴数据。
        :param y_axis:
            y 坐标轴数据。
        :param is_stack:
            数据堆叠，同个类目轴上系列配置相同的 stack 值可以堆叠放置。默认为 False。
        :param kwargs:
        """
        # 断言数据量是否相同, 一一对应
        assert len(x_axis) == len(y_axis)
        kwargs.update(x_axis=x_axis)
        chart = get_all_options(**kwargs)

        if is_stack:
            is_stack = "stack_" + str(self._option['series_id'])
        else:
            is_stack = ""
        xaxis, yaxis = chart['xy_axis']
        self._option.update(xAxis=xaxis, yAxis=yaxis)
        self._option.get('legend')[0].get('data').append(name)

        self._option.get('series').append({
            "type": "bar",
            "name": name,
            "data": y_axis,
            "stack": is_stack,
            "barCategoryGap": bar_category_gap,
            "label": chart['label'],
            "markPoint": chart['mark_point'],
            "markLine": chart['mark_line'],
            "seriesId": self._option.get('series_id'),
        })
        self._config_components(**kwargs)


def screen():
    """
    确定x轴坐标, 通过层级菜单, 筛选指定条件
    :return: 返回筛选后的指定条件 x_category, category_list, type_list
    """

    # 通过层级筛选, 确定筛选条件
    category_dict = {'1': '体型', '2': '身高', '3': '体重', '4': '腹型'}

    # 循环确定x轴坐标显示的分类
    x_id = input("请输入x轴坐标ID{}: ".format(category_dict))
    while x_id not in category_dict.keys():
        print("输入有误, 请重新输入!")
        x_id = input("请输入x轴坐标ID{}: ".format(category_dict))
    x_category = category_dict[x_id]

    # 循环确定筛选条件
    category_list = []
    type_list = []
    while category_dict:
        # 一级筛选
        c_id = input("请输入一级分类ID{}: ".format(category_dict))
        if c_id in category_dict.keys():
            # 二级筛选
            # 若一级分类为 身高, 体重, 则进行范围筛选
            if c_id in ['2', '3']:
                type = input("请输入{}范围(最小值, 最大值, 以空格隔开): ".format(category_dict[c_id]))
            # 若一级分类为 体型, 腹型, 则进行二级分类筛选
            else:
                type = input("请输入{}二级分类(以空格隔开): ".format(category_dict[c_id])).upper()
            type_li = type.split()  # 以空格分隔字符串, 生成多条件列表
            type_list.append(type_li)
            category_list.append(category_dict[c_id])
            category_dict.pop(c_id)
        # 回车键, 返回空字符串, 循环结束
        elif c_id == "":
            break
        else:
            print("输入有误, 请重新输入!")

    print("x轴坐标: {}".format(x_category))
    print("一级分类: {}".format(category_list))
    print("二级分类: {}".format(type_list))

    return x_category, category_list, type_list


def extract(data, fields, x_category, category_list, type_list):
    """
    根据筛选出的条件, 取出符合条件的指定数据, 构造 pandas 的 Series 数据结构
    :param data: 读取Excel表中数据
    :param fields: 字段列表
    :param x_category: x轴坐标
    :param category_list: 筛选后的分一级类列表
    :param type_list: 筛选后的二级分类列表
    :return: x, y
    """

    jywc_series = data[15][1:]  # s1 --> 净腰围差
    id_series = data[0][1:]  # id --> 所有id的Series数据
    id_list = id_series.values  # 所有id列表

    x_column = fields.index(x_category)  # 指定x轴的列索引值
    x_data = data[x_column][1:]  # 根据列索引值取到对应x轴的Series数据
    temp_dict = dict(zip(id_series.values, x_data.values))  # 构造x轴数据对应id的字典--> id: value

    for i in range(len(category_list)):  # i = 0;1;2;3
        column = fields.index(category_list[i])  # 指定类别字段的列索引值
        series = data[column][1:]  # 根据列索引值取到对应列字段的Series数据
        m = []
        # 若一级分类为 身高, 体重, 则遍历范围取值
        if category_list[i] in ['身高', '体重']:
            type_min = int(type_list[i][0])  # 范围最小值
            type_max = int(type_list[i][1])  # 范围最大值
            for j in range(type_min, type_max + 1):
                n = series[series.values == j].index  # 取出指定分类字段对应的ID
                # 一级分类相同, 二级分类不同, 取并集
                m = list(set(m).union(set(n)))  # 取相同分类不同子分类的并集
        else:
            # 若一级分类为 体型, 腹型, 则遍历二级分类取值
            for j in type_list[i]:
                n = series[series.values == j].index  # 取出指定分类字段对应的ID
                m = list(set(m).union(set(n)))  # 取相同分类不同子分类的并集

        # 一级分类不同 取交集
        id_list = list(set(id_list).intersection(set(m)))  # 取不同分类l和m的交集

    # 对筛选结果进行判断
    id_list.sort()
    if id_list:
        print("筛选后的id列表: {}".format(id_list))
    else:
        print("当前筛选条件没有对应数据, 请重新筛选!")

    x_dict = dict(zip(id_list, [temp_dict[i] for i in id_list]))  # 筛选后x轴数据字典

    l = values2keys(x_dict)  # 筛选后x轴数据升序排列后的对应id列表

    x_list = [str(temp_dict[i]) + "({})".format(i) for i in l]  # 最终x轴坐标数据显示

    y_list = [(round(i, 2)) for i in jywc_series[l]]  # 取出指定ID对应的净腰围差, 且保留两位小数

    # 构造pandas中的Series数据结构
    x = pd.Series(x_list)
    y = pd.Series(y_list)

    return x, y


if __name__ == "__main__":

    data = pd.read_excel("test_data.xlsx", header=None)  # 获取Excel数据

    # 确定Excel中所有字段列表
    fields = []
    for i in range(len(data.columns)):
        fields.append(data[i][0])
    # print("所有字段列表: {}".format(fields))

    while True:

        # 通过screen方法, 确定筛选条件
        x_category, category_list, type_list = screen()

        # 通过extract方法, 根据筛选条件, 确定筛选后的数据, 返回Series数据类型
        x, y = extract(data, fields, x_category, category_list, type_list)

        tip_str = ""
        for i in type_list:
            tip_str += '~'.join(i) + '; '

        # 通过pyecharts的Bar类中的方法, 将筛选后的数据动态可视化
        bar = Bar()
        # 显示最大值, 最小值, 平均值, 数据缩放展示
        bar.add('净腰围差( {})'.format(tip_str), x, y, mark_point=["max", "min"], mark_line=["average"],
                is_datazoom_show=True)

        bar.render('show.html')
