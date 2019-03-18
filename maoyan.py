import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}


def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        print('网页请求状态码出错')
        return None
    except RequestException:
        print('网页请求失败了')
        return None


def parse_one_page(html):
    # print(html)
    pattern = re.compile('<dd>.*?board-index.*?(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                    +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                    +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '排名': item[0],
            '图片': item[1],
            '名称': item[2],
            '主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '评分': item[5]+item[6]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    if html:
        for item in parse_one_page(html):
            write_to_file(item)
            print(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    print('抓取成功')
    # pool = Pool()
    # pool.map(main, [i*10 for i in range(10)])
