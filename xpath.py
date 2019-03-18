import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}

text = requests.get('https://maoyan.com/board/4', headers=headers).text
html = etree.HTML(text)
array = html.xpath('//dd')
print(array)
for item in array:
    content = etree.tostring(item).decode('utf-8')
    temp = etree.HTML(content)
    results = temp.xpath(
        '//img/@data-src|'
        + '//p[@class="name"]/a/text()|'
        + '//p[@class="star"]/text()|'
        + '//p[@class="releasetime"]/text()|'
        + '//i[@class="integer"]/text()|'
        + '//i[@class="fraction"]/text()'
    )
    print(results)
