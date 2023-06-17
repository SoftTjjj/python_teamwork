'''
school.py
'''

import json
from time import sleep
import requests

from model_school import School, SchoolConstance


def get_pages() -> list[School]:
    '''
    获取多页的内容
    '''
    result: list[School] = []
    index = 0
    pages = get_page(index)
    while len(pages) != 0:
        result.extend(pages)
        index += 1
        pages = get_page(index)
    return result


def get_page(page: int) -> list[School]:
    '''
    获取第 `page` 页的 20 条结果
    '''
    sleep(1)
    print(f'> 正在获取第 {page} 页的内容')

    ak = 'RcFMxuBRNQ8m7PO7PB2DuMxeibaRqojR'
    params = {
        'query': '学校',
        'tag': '教育培训',
        'region': '南昌',
        'output': 'json',
        'page_num': page,
        'page_size': 20,
        'ak': ak,
    }

    res = requests.get(
        url=f'{SchoolConstance.base_url}/place/v2/search',
        params=params,
        timeout=None,
    )

    schools: list[School] = [
        School(
            name=result['name'],
            latitude=str(result['location']['lat']),
            longitude=str(result['location']['lng']),
        ) for result in res.json()['results']
    ]

    print(f'> 已获取 {len(schools)} 条结果')

    return schools


if __name__ == '__main__':
    schools: list[dict] = [school.__dict__ for school in get_pages()]
    with open('data/schools.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(schools, ensure_ascii=False, indent=2))
