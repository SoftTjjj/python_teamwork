'''
render_hospital.py
'''

import math
from pyecharts import charts, options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from model_building_area import BuildingArea, read_as_building_areas
from model_hospital import Hospital
from utils import get_distance_hav, read_json_file_as_list

class RenderHospitalConstance:
    '''
    存放常数信息
    '''
    area_dict: dict = {
        'donghu': '东湖',
        'gaoxinkaifaqu': '高新开发区',
        'honggutan': '红谷滩',
        'jingkaiqu': '经开区',
        'jinxian': '进贤',
        'nanchangxian': '南昌县',
        'qingshanhu': '青山湖',
        'qingyunpu': '青云谱',
        'wanli': '湾里',
        'xihu': '西湖',
        'xinjian': '新建',
    }


def get_value_of(building_area: BuildingArea, hospitals: list[Hospital]) -> float:


    value: float = 0
    for hospital in hospitals:
        distance: float = get_distance_hav(
            building_area.latitude,
            building_area.longitude,
            hospital.latitude,
            hospital.longitude,
        )
        value += math.exp(-distance**2 / 80)
    print(f'{building_area.name}的价格为 {building_area.price} 权值为 {value:.2f}')
    return round(value, 2)


if __name__ == '__main__':

    data: list[list[float]] = []
    scatter = charts.Scatter(init_opts=opts.InitOpts(
        width='100%',
        height='978px',
        page_title='南昌各地房价与医院距离加权图',
        theme=ThemeType.ESSOS,
    ))
    for area, area_cn in RenderHospitalConstance.area_dict.items():
        building_areas = read_as_building_areas(
            f'./data/building_area/{area}.json')
        scatter.add_xaxis(xaxis_data=[
            building_area.price for building_area in building_areas
        ])
        y_data = []
        for building_area in building_areas:
            y_data.append([
                get_value_of(building_area, [
                    Hospital.from_json(dct)
                    for dct in read_json_file_as_list('./data/hospitals.json')
                ]),
                building_area.name,
            ])
        scatter.add_yaxis(
            series_name=area_cn,
            y_axis=y_data,
            symbol_size=10,
            label_opts=opts.LabelOpts(is_show=False),
        )

    scatter.set_series_opts()
    scatter.set_global_opts(
        title_opts=opts.TitleOpts(title='南昌各地房价与医院距离加权图'),
        xaxis_opts=opts.AxisOpts(
            type_="value",
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        tooltip_opts=opts.TooltipOpts(formatter=JsCode(
            "function (params) {return params.value[2] + ' : ' + params.value[1];}"
        )),
    )
    scatter.render("./output/南昌各地房价与医院距离加权图.html")
