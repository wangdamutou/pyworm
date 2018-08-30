# coding=utf-8

import time
import re
import os
from urllib import request
from bs4 import BeautifulSoup as bs


# 获取页面url列表
def get_url_list(url):
    page_title = ''
    url_list = []
    try:
        resp = request.urlopen(url)
        html_data = resp.read().decode('utf-8')
        # 使用BeautifulSoup库进行html代码解析
        soup = bs(html_data, 'html.parser')
        page_title = soup.find_all('title')[0].get_text()
        # print(str(page_title).strip())
        # 获取id为nowplaying的div
        url_table = soup.find_all('table', class_='olt')
        # 获取class为list-item的列表
        url_td_list = url_table[0].find_all('td', class_='title')
        # print(url_td_list)
        for item in url_td_list:
            a_tag = item.find_all('a')
            url = a_tag[0].get('href')
            url_list.append(url)
    except ConnectionError:
        print('Error.')
    # print(url_list)
    return str(page_title).strip(), url_list


# 获取页面上的图片地址
def get_img_by_url(url):
    # img_dict = {}
    time.sleep(3)
    url_list = []
    try:
        resp = request.urlopen(url)
        html_data = resp.read().decode('utf-8')
        # 使用BeautifulSoup库进行html代码解析
        soup = bs(html_data, 'html.parser')
        # 获取正文区域的div
        image_container_list = soup.find_all('div', class_='image-container')
        if len(image_container_list) == 0:
            return None
        for item in image_container_list:
            img_tag = item.find_all('img')
            img_url = img_tag[0].get('src')
            url_list.append(img_url)
        # img_dict[url[-10:-1]] = url_list
    except ConnectionError:
        print('Error.')
    return url[-10:], url_list


# 根据dict将图片保存至文件
def save_img_to_file(dict, dir_path):
    img_count = 0
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    for k, v in dict.items():
        target_dir = os.path.join(dir_path, k)
        # 如果文件夹已经存在，图片已经下载下来过，如果文件夹不存在则新建文件夹，爬取图片
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
            for img_url in v:
                file_name = img_url[-10:]
                with open(os.path.join(target_dir, file_name), 'wb') as f:
                    f.write(request.urlopen(img_url).read())
                    img_count += 1
    return img_count


# 主方法
def main():
    # 请不要害羞
    # index_url = 'https://www.douban.com/group/haixiuzu/?type=essence#topics'
    # 我们都爱大胸妹
    # index_url = 'https://www.douban.com/group/510760/?type=essence#topics'
    # 女神大本营
    # index_url = 'https://www.douban.com/group/368701/?type=essence#topics'
    # 晒晒你最性感的照片
    # index_url = 'https://www.douban.com/group/DQMQQ/?type=essence#topics'
    # 春天里
    # index_url = 'https://www.douban.com/group/569879/?type=essence#topics'
    index_url_list = ['https://www.douban.com/group/haixiuzu/?type=essence#topics',
                      'https://www.douban.com/group/510760/?type=essence#topics',
                      'https://www.douban.com/group/368701/?type=essence#topics',
                      'https://www.douban.com/group/DQMQQ/?type=essence#topics',
                      'https://www.douban.com/group/569879/?type=essence#topics']
    for index_url in index_url_list:
        page_title, page_list = get_url_list(index_url)
        page_url_dict = {}
        for url in page_list:
            result = get_img_by_url(url)
            if result is not None:
                page_url_dict[result[0]] = result[1]
        dir_path = os.path.join('E:\douban\\', page_title)
        print(page_title, ': ', save_img_to_file(page_url_dict, dir_path))


if __name__ == '__main__':
    main()
