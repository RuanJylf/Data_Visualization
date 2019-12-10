# 测试版

import pandas as pd
from pyecharts.chart import Chart
from pyecharts.option import get_all_options


class Bar(Chart):
    """
    <<< 动态 柱状图/条形图 >>>
    柱状/条形图，通过柱形的高度/条形的宽度来表现数据的大小。
    """

    def __init__(self, title="", subtitle="", **kwargs):
        super(Bar, self).__init__(title, subtitle, **kwargs)

    def add(self, *args, **kwargs):
        self.__add(*args, **kwargs)

    def __add(self, name, x_axis, y_axis, is_stack=False, bar_category_gap="20%",**kwargs):
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
    通过层级菜单, 筛选出指定的条件
    :return: 返回筛选后的指定条件 category_list, type_list
    """

    # 通过层级筛选, 确定筛选条件
    category_dict = {"1": "体型", "2": "身高", "3": "体重", "4": "腹型"}
    category_list = []
    type_list = []
    while category_dict:
        # 一级筛选
        c_id = input("请输入查询的分类ID{}: ".format(category_dict))
        if c_id in category_dict.keys():
            # 二级筛选
            type = input("请输入具体{}, 以空格隔开: ".format(category_dict[c_id])).upper()
            type = type.split()  # 以空格分隔字符串, 生成多条件列表
            type_list.append(type)
            category_list.append(category_dict[c_id])
            category_dict.pop(c_id)
        # 回车键, 返回空字符串, 循环结束
        elif c_id == "":
            break
        else:
            print("输入的分类ID有误!!")
    print("筛选的分类: {}".format(category_list))
    print("筛选的具体分类: {}".format(type_list))

    return category_list, type_list


def extract(data, fields, category_list, type_list):
    """
    根据筛选出的条件, 取出符合条件的指定数据, 构造 pandas 的 Series 数据结构
    :param data: 读取Excel表中数据
    :param fields: 字段列表
    :param category_list: 筛选后的分一级类列表
    :param type_list: 筛选后的二级分类列表
    :return:
    """

    s1 = data[15][1:]  # s1 --> 净腰围差
    s2 = data[6][1:]  # s2 --> 净腰围

    l = data[0][1:].index  # 所有的id列表
    for i in range(len(category_list)):
        column = fields.index(category_list[i])  # 指定类别字段的列索引值
        s = data[column][1:]  # 根据列索引值取到对应列字段的数据
        m = []
        # 一级分类相同, 二级分类不同, 取并集
        for j in type_list[i]:
            if category_list[i] in ["身高", "体重"]:
                type = float(j)
            else:
                type = j
            n = s[s.values == type].index  # 取出指定分类字段对应的ID
            m = list(set(m).union(set(n)))  # 取相同分类不同子分类的并集
        # 一级分类不同 取交集
        l = list(set(l).intersection(set(m)))  # 取不同分类l和m的交集

    # 对筛选结果进行判断
    if l:
        l.sort()  # 筛选后 id 排序, 便于展示
        print("筛选后的id列表: {}".format(l))
    else:
        print("当前筛选条件没有对应数据, 请重新筛选!")

    l1 = [(round(i, 2)) for i in s1[l]]  # 取出指定ID对应的净腰围差, 且保留两位小数
    l2 = [(round(i, 2)) for i in s2[l]]  # 取出指定ID对应的净腰围, 且保留两位小数

    # 构造pandas中的Series数据结构
    x = pd.Series(l)
    y1 = pd.Series(l1)
    y2 = pd.Series(l2)

    return x, y1, y2


if __name__ == "__main__":

    data = pd.read_excel("test_data.xlsx", header=None)  # 获取Excel数据

    # 确定Excel中所有字段列表
    fields = []
    for i in range(len(data.columns)):
        fields.append(data[i][0])
    print("所有字段列表: {}".format(fields))

    while True:
        # 通过screen方法, 确定筛选条件
        category_list, type_list = screen()

        # 通过extract方法, 根据筛选条件, 确定筛选后的数据, 返回Series数据类型
        x, y1, y2 = extract(data, fields, category_list, type_list)

        # 通过pyecharts的Bar类中的方法, 将筛选后的数据动态可视化
        bar = Bar()
        # 显示最大值, 最小值, 平均值, 数据缩放展示
        bar.add('净腰围差', x, y1, mark_point=["max","min"],mark_line=["average"], is_datazoom_show=True)
        bar.add('净腰围', x, y2, mark_point=["max","min"],mark_line=["average"], is_datazoom_show=True)

        bar.render('show.html')
