import requests
import bs4


def open_url(url):
    # 使用代理
    # proxies = {"http" : "127.0.0.1:1080", "https": "127.0.0.1:1080"}
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    # res = requests.get(url, headers=headers, proxies=proxies)
    res = requests.get(url, headers=headers)
    return res


def find_movies(res):
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # 电影名
    movies = []
    targets = soup.find_all('div', class_="hd")
    for each in targets:
        movies.append(each.a.span.text)

    # 评分
    ranks = []
    targets = soup.find_all("span", class_='rating_num')
    for each in targets:
        ranks.append('评分：%s' % each.text)  # 字符串格式符%s

    # 资料
    messages = []
    targets = soup.find_all('div', class_='bd')
    for each in targets:
        try:
            messages.append(each.p.text.split('\n')[1].strip() + each.p.text.split('\n')[2].strip())
        except:
            continue
    result = []
    length = len(movies)
    for i in range(length):
        result.append(movies[i] + ranks[i] + messages[i] + '\n')

    return result


# 找出一共有多少个页面
def find_depth(res):
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    # 一个标签的上个节点或者下一个节点通常都是空格
    # 连续两次才能拿到相邻的节点
    # 此行代码的意思是获取一个class = "next" 的上上个节点，所以就是上个<a href="xxx">10</a> a标签
    depth = soup.find('span', class_="next").previous_sibling.previous_sibling.text
    return int(depth)  # 10


def main():
    host = "https://movie.douban.com/top250"
    res = open_url(host)
    depth = find_depth(res)
    result = []
    for i in range(depth):
        url = host + '/?start=' + str(25 * i)
        res = open_url(url)
        # extend一次性追加另一个序列中的多个值
        result.extend(find_movies(res))
    with open("豆瓣TOP250电影.tex", "w", encoding="utf-8") as f:
        for each in result:
            f.write(each)
    print("抓取完成")


if __name__ == '__main__':
    main()
