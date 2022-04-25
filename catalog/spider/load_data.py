# requests 获取网页信息
# -*- coding: utf-8 -*-
import requests
import time
import csv
import json
import os
import django
from bs4 import BeautifulSoup
# from urllib.request import urlretrieve
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localMovie.settings')
django.setup()
from catalog.models import Movie

url_top250 = [
        'https://movie.douban.com/top250',
        'https://movie.douban.com/top250?start=25&filter=',
        'https://movie.douban.com/top250?start=50&filter=',
        'https://movie.douban.com/top250?start=75&filter=',
        'https://movie.douban.com/top250?start=100&filter=',
        'https://movie.douban.com/top250?start=125&filter=',
        'https://movie.douban.com/top250?start=150&filter=',
        'https://movie.douban.com/top250?start=175&filter=',
        'https://movie.douban.com/top250?start=200&filter=',
        'https://movie.douban.com/top250?start=225&filter=',
]

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"
}
cookies = {
    "cookie": "bid=p3-BYv-dPdk; ll=\"108304\"; push_noty_num=0; push_doumail_num=0; douban-fav-remind=1; __gads=ID=7652455ee9cd37f8-2262d3cb15d100a6:T=1647777132:RT=1647777132:S=ALNI_MavdzmL299fqlBb-yHKdPQhoX_0xQ; __utmv=30149280.25498; _ga=GA1.2.1995445140.1647777134; _gid=GA1.2.643440456.1650353372; __utmz=30149280.1650353447.20.10.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.2fad=%5B%22%22%2C%22%22%2C1650437179%2C%22https%3A%2F%2Fsec.douban.com%2F%22%5D; _pk_id.100001.2fad=b3fdeb726be583cf.1647864638.5.1650437179.1650357265.; ap_v=0,6.0; __utma=30149280.1995445140.1647777134.1650353447.1650521293.21; __utmb=30149280.0.10.1650521293; __utmc=30149280; apiKey=; curren_area_code=+86; curren_phone=15538009337; dbcl2=\"254988002:12DwC5aq2gA\"; isNoPwd=true; code=9483; ck=z1HW"
}
fieldnames = ['评分', '制片国家/地区', '编剧', '片长', '评论人数', '导演', '类型', '又名', '语言', 'IMDb', '上映日期', '片名', '主演']


def load_img(img_url, name):
    # urlretrieve(img_url, '../static/image/' + name + '.jpg')
    return

# 把列表切割成字典
def parse_text(info):
    listt = [item.strip()for item in  info.split('\n') if item.strip(' ')]
    listt = [item.split(':') for item in listt]
    listt = [items for items in listt if len(items) == 2 and items[0].strip() and items[1].strip()]
    dinfo = dict(listt)
    return dinfo


def write_csv(csv_url, info_list):
    with open(csv_url, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for elem in info_list:
            writer.writerow(elem)


def load_detail(detail_url, movie_name):
    detail_response = requests.get(detail_url, headers=headers)
    detail_html = detail_response.text
    detail_soup = BeautifulSoup(detail_html, "html5lib")
    detail = detail_soup.find("div", id="info")
    text_info = detail.get_text()
    dic_info = parse_text(text_info)
    mscore = detail_soup.find('div', class_="rating_self clearfix")
    score = mscore.find(property="v:average").get_text()
    votes = ""
    if score != "":
        votes = mscore.find(property="v:votes").get_text()
    dic_info['评分'] = score
    dic_info['评论人数'] = votes
    dic_info['片名'] = movie_name
    for key in list(dic_info.keys()):
        if key not in fieldnames:
            dic_info.pop(key)
    return dic_info


# 加载TOP250电影数据
def load_top250():
    movie_lists = []
    for url in url_top250:
        response = requests.get(url, headers=headers)
        # print(response)
        html = response.text
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        movie_list = soup.find("div", class_="article")
        movies = movie_list.find_all("div", class_="item")

        for movie in movies:
            # 获取电影名
            movie_name = movie.find("span", class_="title").get_text()
            movie_name = movie_name.strip()
            movie_name = str(movie_name).replace('/', ' ')
            # 电影详情url
            detail_url = movie.find("a").get("href")
            dic_info = load_detail(detail_url, movie_name)
            movie_lists.append(dic_info)
            print(detail_url)
            # 电影图片url
            img_url = movie.find("img").get("src")
            load_img(img_url, movie_name)
            time.sleep(3)
    # 将数据存入文件
    write_csv("movie_data(top250).csv", movie_lists)
    # file = open("movie_data.csv", 'r', encoding='utf-8')
    # while True:
    #     text = file.readline()  # 只读取一行内容
    #     # 判断是否读取到内容
    #     if not text:
    #         break
    #     print(text)


# 爬取热门电影数据
def load_hot():
    num = 0
    for i in range(8, 10):
        movie_lists = []
        response = requests.get("https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%B3%B0%E5%9B%BD&sort=recommend&page_limit=20&page_start="
                                + str(i * 20), headers=headers)
        json_data = response.text
        data = json.loads(json_data)
        movies = data['subjects']
        for movie in movies:
            # 获取电影名
            movie_name = movie['title']
            movie_name = movie_name.strip()
            movie_name = str(movie_name).replace('/', ' ')
            # 电影详情url
            detail_url = movie['url']
            dic_info = load_detail(detail_url, movie_name)
            movie_lists.append(dic_info)
            num = num + 1
            print(movie_name, num, detail_url)
            # 电影图片url
            img_url = movie['cover']
            load_img(img_url, movie_name)
            time.sleep(3)
        # 将数据存入文件
        write_csv("movie_data(thailand" + str(i + 1) + ").csv", movie_lists)


def add_records():
    movies = Movie.objects.all()
    total = 0
    for movie in movies:
        total += 1
        if total <= 13767:
            continue
        response = requests.get(
            "https://movie.douban.com/subject/" + str(movie.movie_id), headers=headers, cookies=cookies)
        data = response.text
        soup = BeautifulSoup(data, "html5lib")
        detail = soup.find("div", id="subject-header-container")
        if detail is None:
            time.sleep(2)
            continue
        detail = detail.find("a", class_="sub-cover")
        # 电影图片url
        img_url = detail.find("img").get("src")
        print(total, img_url)
        movie.movie_url = img_url
        try:
            movie.save()
        except ValueError as err:
            print(err)
        time.sleep(2)

add_records()

# file = open("movie_data(korea).csv", 'r', encoding='utf-8')
# while True:
#     text = file.readline()  # 只读取一行内容
#     # 判断是否读取到内容
#     if not text:
#         break
#     print(text)


