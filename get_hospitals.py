'''
hospital.py
'''
from __future__ import annotations

import json
import re
import requests
from lxml import etree

from model_hospital import Hospital, HospitalConstance


def get_hospitals() -> None:
    '''
    获取南昌市所有医院的信息并保存为 json 文件
    '''

    json_path: str = './data/hospitals.json'

    # 发送请求
    res_text = requests.get(
        url=HospitalConstance.base_url,
        headers=HospitalConstance.headers,
        timeout=None,
    ).text

    # 获取 node 树，并通过 xpath 获取医院列表
    tree = etree.HTML(res_text)
    li_list: list = tree.xpath(
        '//*[@id="el_result_content"]/div/div[2]/div[2]/div[2]/ul/li')

    hospitals: list[dict] = []

    for li in li_list:
        position = get_position_by(li.xpath('a/@href')[0])
        if position is not None:
            name = li.xpath('a/text()')[0]
            hospital = Hospital(name, position[0], position[1])
            hospitals.append(hospital.__dict__)

    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(hospitals, ensure_ascii=False, indent=2))


def get_position_by(url: str) -> tuple[str, str] | None:
    '''
    根据 `url` 获取经纬度
    '''
    url = url.replace('.html', '/jieshao.html')
    print(f'> 正在获取 {url}')
    res: str = requests.get(
        url,
        headers=HospitalConstance.headers,
        timeout=None,
    ).text
    tree = etree.HTML(res)
    try:
        map_url = tree.xpath(
            '//*[@id="app"]/div[3]/div[1]/div[1]/div[1]/div/p/span/a/@href')[0]
    except IndexError:
        return None
    reg = re.compile(r'location=(.*),(.*?)&')
    return reg.findall(map_url)[0]


if __name__ == '__main__':
    get_hospitals()
