#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals

import json
import codecs
from pyecharts import Map


def test_map_show_label():
    # show label
    value = [155, 10, 66, 78]
    attr = ["福建", "山东", "北京", "上海"]
    map = Map("全国地图示例", width=1200, height=600)
    map.add("", attr, value, maptype='china', is_label_show=True)
    map.render()


def test_map_combine_with_visualmap():
    value = [155, 10, 66, 78, 33, 80, 190, 53, 49.6]
    attr = ["福建", "山东", "北京", "上海", "甘肃",
            "新疆", "河南", "广西", "西藏"]
    map = Map("Map 结合 VisualMap 示例", width=1200, height=600)
    map.add("", attr, value, maptype='china', is_visualmap=True,
            visual_text_color='#000')
    map.render()


def test_echarts_position_in_render_html():
    value = [20, 190, 253, 77, 65]
    attr = ['汕头市', '汕尾市', '揭阳市', '阳江市', '肇庆市']
    map = Map("广东地图示例", width=1200, height=600)
    map.add("", attr, value, maptype='广东', is_map_symbol_show=False,
            is_visualmap=True, visual_text_color='#000')
    map.render()
    with codecs.open('render.html', 'r', 'utf-8') as f:
        actual_content = f.read()
        echarts_position = actual_content.find('exports.echarts')
        guangdong_position = actual_content.find(json.dumps('广东'))
        assert echarts_position < guangdong_position
        assert '"showLegendSymbol": false' in actual_content


def test_city_map():
    value = [1]
    attr = ["渝水区"]
    map = Map("新余地图示例", width=1200, height=600)
    map.add("", attr, value, maptype='新余', is_visualmap=True,
            visual_text_color='#000')
    # To avoid potential pinyin crash, all cities have a province prefix
    assert "jiang1_xi1_xin1_yu2" in map._repr_html_()


def test_world_map():
    value = [95.1, 23.2, 43.3, 66.4, 88.5, 0.1]
    attr = [
        "China", "Canada", "Brazil", "Russia",
        "United States", "Unknown Country"
    ]
    map = Map("世界地图示例", width=1200, height=600)
    map.add("", attr, value, maptype="world", is_visualmap=True,
            visual_text_color='#000')
    map.render()

    with codecs.open('render.html', 'r', 'utf-8') as f:
        actual_content = f.read()
        # test register map
        assert "registerMap(\"world\"," in actual_content
        # test non-existent country
        assert "Russia" in actual_content
        assert "Unknown Country', " not in actual_content


def test_china_map():
    value = [155, 10, 66, 78]
    attr = ["福建", "山东", "北京", "上海"]
    map = Map("全国地图示例", width=1200, height=600)
    map.add("", attr, value, maptype='china')
    map.render()

    with codecs.open('render.html', 'r', 'utf-8') as f:
        actual_content = f.read()
        # test register map
        assert "registerMap(\"china\"," in actual_content
        # 福建省
        assert "\u798f\u5efa" in actual_content
        # 汕头市
        assert "\u4e0a\u6d77" in actual_content
