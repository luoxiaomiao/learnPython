import requests
import os
import re
from urllib.parse import urlencode
from hashlib import md5
from multiprocessing.pool import Pool
from requests import codes


def get_page(offset):
    params = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': KEYWORD,
        'autoload': 'true',
        'count': 20,
        'cur_tap': 1,
        'en_qc': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.json())
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                origin_image = re.sub('list', 'origin', image.get('url'))
                yield {
                    'image': origin_image,
                    'title': title
                }


def save_image(item):
    img_path = 'img' + os.path.sep + item.get('title')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        response = requests.get(item.get('image'))
        if response.status_code == codes.ok:
            file_path = img_path + os.path.sep + '{0}.{1}'.format(md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 7
KEYWORD = '汽车'

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END+1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
