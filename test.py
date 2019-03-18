import requests
import bs4

host = "https://movie.douban.com/top250"
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
res = requests.get(host, headers=headers)
soup = bs4.BeautifulSoup(res.text, "html.parser")
depth = soup.find('span', class_="next").previous_sibling.previous_sibling.text
print(depth)

span = soup.find('span', class_="next")
print(span)
print("----------")
pre = span.previous_sibling
print(pre)
print("----------")
pre2 = span.previous_sibling.previous_sibling
print(pre2)
print("----------")
text = pre2.text
print(text)
print("----------")





