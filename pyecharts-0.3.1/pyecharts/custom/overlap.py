# coding=utf-8

import copy
from pyecharts.constants import PAGE_TITLE
from pyecharts.base import Base


class Overlap(Base):
    """
    用户可以自定义结合 Line/Bar/Kline, Scatter/EffectScatter 图表，
    将不同类型图表画在一张图上。利用第一个图表为基础，往后的数据都将
    会画在第一个图表上。
    """
    def __init__(self, page_title=PAGE_TITLE,
                 width=800,
                 height=400,
                 jshost=None):
        super(Overlap, self).__init__(
            width=width, height=height, jshost=jshost
        )
        self._page_title = page_title

    def add(self, chart,
            xaxis_index=0,
            yaxis_index=0,
            is_add_xaxis=False,
            is_add_yaxis=False):
        """

        :param chart:
            图形实例
        :param xaxis_index:
            x 坐标轴索引，默认为 0
        :param yaxis_index:
            y 坐标轴索引，默认为 0
        :param is_add_xaxis:
            是否新增一个 x 坐标轴，默认为 False
        :param is_add_yaxis:
            是否新增一个 y 坐标轴，默认为 False
        """
        if not self._option:
            self._option = copy.deepcopy(chart.options)
            self._series_id = self._option.get('series')[0].get('seriesId')
            self._js_dependencies = chart.js_dependencies
        else:
            _series = (
                chart.options.get('legend')[0].get('data'),
                chart.options.get('series'),
                chart.options.get('xAxis')[0],
                chart.options.get('yAxis')[0],
                is_add_xaxis,
                is_add_yaxis,
                xaxis_index,
                yaxis_index
            )
            self.__custom(_series)
            self._js_dependencies = self._js_dependencies.union(
                chart.js_dependencies)

    def __custom(self, series):
        """ Appends the data for the series of the chart type

        :param series:
            series data
        """
        (_name, _series, _xaxis, _yaxis, is_add_xaxis, is_add_yaxis,
         _xaxis_index, _yaxis_index) = series
        for n in _name:
            self._option.get('legend')[0].get('data').append(n)
        for s in _series:
            s.update(xAxisIndex=_xaxis_index, yAxisIndex=_yaxis_index,
                     seriesId=self._series_id)
            self._option.get('series').append(s)

        if is_add_xaxis:
            self._option.get('xAxis').append(_xaxis)
        if is_add_yaxis:
            self._option.get('yAxis').append(_yaxis)
