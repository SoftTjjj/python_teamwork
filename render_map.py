'''
render_map.py
'''

from pyecharts import charts, options

from get_building_areas import BuildingAreaConstance, read_json_file_as_list


def add_point(geo, path, locate):
    '''
    在图 `geo` 上加入系列 `locate`，其数据读取自 `path`
    '''
    data = read_json_file_as_list(path)
    data_pair_list: list = []
    for item in data:
        name = item['name']
        latitude = item['latitude']
        longitude = item['longitude']
        if latitude != 'None' and longitude != 'None':
            geo.add_coordinate(name, float(longitude), float(latitude))
            data_pair_list.append((name, locate))
    geo.add(series_name=locate, data_pair=data_pair_list, symbol_size=7)


if __name__ == '__main__':
    geo = charts.Geo(init_opts=options.InitOpts(
        page_title='南昌楼市数据', width='100%', height='958px'))

    geo.set_global_opts(
        title_opts=options.TitleOpts(
            title='南昌楼市数据',
            pos_left='50%',
            pos_top='20px',
        ),
        legend_opts=options.LegendOpts(
            is_show=True,
            pos_left='10%',
            pos_top='20%',
            orient='vertical',
        ),
        tooltip_opts=options.TooltipOpts(
            is_show=True,
            formatter='{a}:{b}',
        ),
    )

    geo.add_schema(maptype='南昌')

    for area in BuildingAreaConstance.areas:
        add_point(geo, f'./data/building_area/{area}.json', '楼盘')
    add_point(geo, './data/hospitals.json', '医院')
    add_point(geo, './data/markets.json', '商场')
    add_point(geo, './data/schools.json', '学校')

    geo.set_series_opts(label_opts=options.LabelOpts(is_show=False))

    geo.render('./output/render_map.html')
