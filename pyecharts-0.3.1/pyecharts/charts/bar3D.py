# coding=utf-8

from pyecharts.chart import Chart
from pyecharts.option import get_all_options


class Bar3D(Chart):
    """
    <<< 3D 柱状图 >>>
    """

    def __init__(self, title="", subtitle="", **kwargs):
        super(Bar3D, self).__init__(title, subtitle, **kwargs)
        self._js_dependencies.add('echartsgl')

    def add(self, *args, **kwargs):
        self.__add(*args, **kwargs)

    def __add(self, name, x_axis, y_axis, data,
              grid3d_opacity=1,
              grid3d_shading='color',
              **kwargs):
        """

        :param name:
            系列名称，用于 tooltip 的显示，legend 的图例筛选。
        :param x_axis:
            x 坐标轴数据。需为类目轴，也就是不能是数值。
        :param y_axis:
            y 坐标轴数据。需为类目轴，也就是不能是数值。
        :param data:
            数据项，数据中，每一行是一个『数据项』，每一列属于一个『维度』。
        :param grid3d_opacity:
            3D 笛卡尔坐标系组的透明度（柱状的透明度），默认为 1，完全不透明。
        :param grid3d_shading:
            三维柱状图中三维图形的着色效果。
            color：
                只显示颜色，不受光照等其它因素的影响。
            lambert：
                通过经典的 lambert 着色表现光照带来的明暗。
            realistic：
                真实感渲染，配合 light.ambientCubemap 和 postEffect 使用可以让
                展示的画面效果和质感有质的提升。ECharts GL 中使用了基于物理的渲
                染（PBR）来表现真实感材质。
        :param kwargs:
        """
        kwargs.update(xaxis3d_type='category',
                      yaxis3d_type='category',
                      zaxis3d_type='value')
        chart = get_all_options(**kwargs)

        self._option.get('legend')[0].get('data').append(name)
        self._option.update(
            xAxis3D=chart['xaxis3D'],
            yAxis3D=chart['yaxis3D'],
            zAxis3D=chart['zaxis3D'],
            grid3D=chart['grid3D']
        )
        self._option.get('xAxis3D').update(data=x_axis)
        self._option.get('yAxis3D').update(data=y_axis)

        self._option.get('series').append({
            "type": "bar3D",
            "name": name,
            "data": data,
            "label": chart['label'],
            "shading": grid3d_shading,
            "itemStyle": {"opacity": grid3d_opacity}
        })
        self._config_components(**kwargs)
