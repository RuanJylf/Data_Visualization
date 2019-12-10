# coding=utf-8

from PIL import Image

from pyecharts.chart import Chart
from pyecharts.option import get_all_options


class Scatter(Chart):
    """
    <<< 散点图 >>>

    直角坐标系上的散点图可以用来展现数据的 x，y 之间的关系，如果数据项有多个维度，
    可以用颜色来表现，利用 geo 组件。
    """
    def __init__(self, title="", subtitle="", **kwargs):
        super(Scatter, self).__init__(title, subtitle, **kwargs)

    def add(self, *args, **kwargs):
        self.__add(*args, **kwargs)

    def __add(self, name, x_axis, y_axis, extra_data=None,
              symbol_size=10,
              **kwargs):
        """

        :param name:
            系列名称，用于 tooltip 的显示，legend 的图例筛选。
        :param x_axis:
            x 坐标轴数据。
        :param y_axis:
            y 坐标轴数据。
        :param extra_data:
            第三维度数据，x 轴为第一个维度，y 轴为第二个维度。（可在 visualmap 中
            将视图元素映射到第三维度）。
        :param symbol_size:
            标记图形大小，默认为 10。
        :param kwargs:
        """
        assert len(x_axis) == len(y_axis)
        kwargs.update(type="scatter", x_axis=x_axis)
        chart = get_all_options(**kwargs)

        xaxis, yaxis = chart['xy_axis']
        self._option.update(xAxis=xaxis, yAxis=yaxis)
        self._option.get('legend')[0].get('data').append(name)

        if extra_data:
            _data = [list(z) for z in zip(x_axis, y_axis, extra_data)]
        else:
            _data = [list(z) for z in zip(x_axis, y_axis)]

        self._option.get('series').append({
            "type": "scatter",
            "name": name,
            "symbol": chart['symbol'],
            "symbolSize": symbol_size,
            "data": _data,
            "label": chart['label'],
            "seriesId": self._option.get('series_id'),
        })
        self._config_components(**kwargs)

    def draw(self, path, color=None):
        """ 将图片上的像素点转换为数组，如 color 为（255,255,255）时只保留非白色像素点的
        坐标信息返回两个 k_lst, v_lst 两个列表刚好作为散点图的数据项

        :param path:
            转换图片的地址
        :param color:
            所要排除的颜色
        :return:
            转换后的数组
        """
        color = color or (255, 255, 255)
        im = Image.open(path)
        width, height = im.size
        imarray = im.load()
        # 垂直翻转图片
        for x in range(width):
            for y in range(height):
                if y < int(height / 2):
                    (imarray[x, y], imarray[x, height-y-1]) = (
                        imarray[x, height-y-1], imarray[x, y])
        # [:3] 代表着 R, G, B 三原色
        result = [(x, y) for x in range(width) for y in range(height)
                  if imarray[x, y][:3] != color]
        return self.cast(result)
