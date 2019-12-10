# Data_Visualization
筛选 Excel 文件数据, 利用 pyecharts 进行动态可视化展示!

## 1. 运行文件
找到当前目录中的data_visualization.py文件, 双击打开, run即可!

## 2. 通过层级菜单, 确定筛选条件

### 一级菜单: '1': '体型', '2': '身高', '3': '体重', '4': '腹型'
* 输入分类对应数字, 进入相应的二级菜单;  
* 当四种条件都选完, 或者按下回车键, 当前筛选完毕;
* 当不选对应的一级分类时, 默认选择全部的二级分类.

### 二级菜单: 根据一级菜单所选分类, 输入二级分类
* 当需输入多个二级分类时, 用空格隔开;  
* 体型分类中, 二级分类输入时大小写皆可, 但须在每种二级分类末尾加"体", 如: ty+体;
* 身高, 体重分类的二级分类只需直接输入数字即可, 如: 180, 60;
* 腹型分类中, 可输入 "平坦", "凸肚", "腹肌" 三种二级分类.

## 3. 查看数据动态可视化
* 运行程序, 筛选条件后, 找到当前目录下的show.html文件, 双击打开, 找到右上角浏览器图标,  
点击对应浏览器图标打开网页即可;
* 数据动态可视化页面: x轴为id值, y轴为净腰围差和净腰围, 图中还显示筛选数据的最大值, 最小值, 平均值;  
* 点击顶部不同类型颜色图标, 可以隐藏对应数据柱形图; 滑动底部, 可以选择展示指定范围对应的数据柱形图;
* 鼠标滑动到某一柱形, 可显示相应id对应的数据字段类型和值;
* 右侧工具栏, 可以下载当前图片, 还原初始状态, 显示数据视图.


