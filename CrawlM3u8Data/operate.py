import requests
import time
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}


def index(app_id, course_id):
    """
    url get info
    :param app_id:
    :param course_id:
    :return: chapter_id course_id app_id
    """

    data = {
        'app_id': app_id,
        'course_id': course_id,
        'order': 'asc',
        'p_id': '0',
        'page': '1',
        'page_size': '50',
        'resource_id': '',
    }

    response = requests.post(
        f'https://{app_id}.pc.xiaoe-tech.com/xe.course.business.avoidlogin.e_course.resource_catalog_list.get/1.0.0',
        headers=headers,
        data=data
    )

    data_list = []
    for data in response.json()['data']['list']:
        data_list.append({
            'chapter_id': data['chapter_id'],
            'course_id': data['course_id'],
            'app_id': data['app_id'],
            'title': data['sort_c'] + '. ' + data['chapter_title'],
        })

    return data_list


def m3u8_path(cookies, params):
    headers['cookie'] = cookies

    params = {
        'app_id': params['app_id'],
        'alive_id': params['chapter_id'],
        'course_id': params['course_id'],
    }

    response = requests.get(
        'https://appgpq2ymld6587.pc.xiaoe-tech.com/_alive/api/get_lookback_list',
        params=params,
        headers=headers,
    )

    time_info = str(int(time.time() * 1000))
    uuid = re.findall('"user_id":"(.*?)"', cookies)[0]
    m3u8_url = response.json()['data'][-1]['line_sharpness'][0]['url'] + f'&time={time_info}&uuid={uuid}'

    del headers['cookie']

    return m3u8_url
