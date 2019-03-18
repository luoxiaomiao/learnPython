import requests
import re

content = requests.get('https://search.bilibili.com/all?keyword=%E7%88%AC%E8%99%AB&from_source=banner_search&spm_id_from=333.334.b_62616e6e65725f6c696e6b.1').text
pattern = re.compile('<li.*?<a\stitle="(.*?)"\shref="//(.*?)"', re.S)
results = re.findall(pattern, content)
for result in results:
    name, url = result
    print(name, url)
