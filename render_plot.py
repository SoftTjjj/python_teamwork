'''
render_plot.py
'''

import numpy as np
import pandas as pd
from pyecharts.charts import Bar, Line, Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType


class RenderPlotConstance:
    '''
    存放常数信息
    '''
    areas = [
        'donghu', 'gaoxinkaifaqu', 'honggutan', 'jingkaiqu', 'jinxian',
        'nanchangxian', 'qingshanhu', 'qingyunpu', 'wanli', 'xihu', 'xinjian'
    ]
    columns = ['avg', 'max', 'min']
    areas_cn = [
        '东湖', '高新开发区', '红谷滩', '经开区', '进贤', '南昌县', '青山湖', '青云谱', '湾里', '西湖',
        '新建'
    ]


def data_clean() -> list:
    '''
    清洗数据
    '''
    # 第一批清洗：得到南昌各地房价的最大值、最小值和平均值
    data_list = np.zeros((len(RenderPlotConstance.areas), 3))
    for i in range(len(RenderPlotConstance.areas)):
        df = pd.read_json(
            f'./data/building_area/{RenderPlotConstance.areas[i]}.json',
            encoding='utf-8',
            orient='records',
        )
        area_price_df = df.loc[:, 'price']
        data_list[i][0] = f'{area_price_df.mean():.2f}'
        data_list[i][1] = area_price_df.max()
        data_list[i][2] = area_price_df.min()

    area_dfs = pd.DataFrame(
        data=data_list,
        index=RenderPlotConstance.areas,
        columns=RenderPlotConstance.columns,
    )

    # 第二批清洗：得到南昌各地楼盘名称和具体价格
    building_cnts = np.zeros(
        len(RenderPlotConstance.areas),
        dtype=int,
    )
    for i in range(len(RenderPlotConstance.areas)):
        df = pd.read_json(
            f'./data/building_area/{RenderPlotConstance.areas[i]}.json',
            encoding='utf-8',
            orient='records',
        )
        data = {'name': list(df.name), 'price': list(df.price)}
        dfs = pd.DataFrame(data=data)
        # 统计南昌各地区楼盘个数
        building_cnts[i] = int(dfs.shape[0])

    return [area_dfs, building_cnts]


class RenderPlot:
    '''
    渲染
    '''

    def __init__(self):
        data: list = data_clean()
        area_dfs = data[0]
        self.avg_ = list(area_dfs.loc[:, 'avg'])
        self.max_ = list(area_dfs.loc[:, 'max'])
        self.min_ = list(area_dfs.loc[:, 'min'])
        self.building_cnts = data[1]

    def draw_bar(self) -> None:
        '''
        南昌各地房价对比条形图
        '''
        bar = Bar(init_opts=opts.InitOpts(
            page_title='南昌各地房价对比条形图',
            width='100%',
            height='978px',
            theme=ThemeType.ESSOS,
        ))

        bar.add_xaxis(RenderPlotConstance.areas_cn)
        bar.add_yaxis('平均房价', self.avg_)
        bar.add_yaxis('最高房价', self.max_)
        bar.add_yaxis('最低房价', self.min_).reversal_axis()

        # 系列配置项
        bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))

        # 全局配置项
        bar.set_global_opts(
            # 标题配置
            title_opts=opts.TitleOpts(title='南昌各地房价对比条形图'),
            datazoom_opts=opts.DataZoomOpts(
                is_show=True,
                range_start=0,
                range_end=60,
            ),
        )
        bar.render('./output/南昌各地房价对比条形图.html')

    def draw_line(self) -> None:
        '''
        南昌各地房价对比折线图
        '''
        line = Line(init_opts=opts.InitOpts(
            page_title='南昌各地房价对比折线图',
            width='100%',
            height='978px',
            theme=ThemeType.ESSOS,
        ))
        line.add_xaxis(RenderPlotConstance.areas_cn)
        line.add_yaxis('平均房价', y_axis=self.avg_)
        line.add_yaxis('最高房价', y_axis=self.max_)
        line.add_yaxis('最低房价', y_axis=self.min_)
        line.set_global_opts(
            title_opts=opts.TitleOpts(title='南昌各地房价对比折线图'),
            # 提示线
            tooltip_opts=opts.TooltipOpts(trigger='axis'),
            # 坐标轴配置
            xaxis_opts=opts.AxisOpts(
                is_show=True,  # 显示x轴
                type_='category',  # 显示离散数据类型
                axislabel_opts=opts.LabelOpts(rotate=45)  # 坐标轴标签旋转
            ),
            datazoom_opts=opts.DataZoomOpts(
                is_show=True,
                type_='slider',
                is_realtime=True,
                range_start=0,
                range_end=100,
            ),
        )
        line.render('./output/南昌各地房价对比折线图.html')

    def draw_pie(self) -> None:
        '''
        南昌各地拥有楼盘占比图
        '''
        building_cnts = [int(value) for value in self.building_cnts]
        pie = Pie(init_opts=opts.InitOpts(
            page_title='南昌各地拥有楼盘占比图',
            width='100%',
            height='978px',
            theme=ThemeType.ESSOS,
        ))
        pie.add('各地楼盘个数占比', [
            list(x) for x in zip(RenderPlotConstance.areas_cn, building_cnts)
        ])
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{c}'))
        pie.set_global_opts(title_opts=opts.TitleOpts(
            title='南昌各地拥有楼盘占比图',
            pos_top='30px',
        ))
        pie.render('./output/南昌各地拥有楼盘占比图.html')


if __name__ == '__main__':
    draw = RenderPlot()
    draw.draw_bar()
    draw.draw_line()
    draw.draw_pie()
