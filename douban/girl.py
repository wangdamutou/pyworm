# coding=utf-8

import time
import hashlib
import re
import os
import json
import requests
from urllib import request
from bs4 import BeautifulSoup as bs


# 登录豆瓣网站
def login():
    url = 'https://accounts.douban.com/login'
    payload = {
        'source': 'None',
        'redir': 'https://www.douban.com/',
        'form_email': 'wuyaxiong',
        'form_password': 'wl151734613057',
        'captcha-solution': 'sneeze',
        'captcha-id': 'Hccs5LSGXmdN34ZhGuSQKhfz:en',
        'login': '登录'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36'}
    resp = requests.post(url, data=payload, headers=headers)
    print(resp.encoding)
    print(resp.status_code)
    # print(resp.json())
    print(requests.codes.ok)  # 此处结果为200
    # print(resp.status_code == requests.codes.ok)
    # print(resp.raise_for_status())
    print(resp.cookies)
    print(resp.history)
    print(resp.headers)
    print(resp.content)
    # print(resp.text)
    print(resp.url)


# 从文件中获取已经爬取的url的哈希值
def get_hash_list(file_path):
    hash_list = []
    with open(file_path, 'rb') as f:
        for line in f.readlines():
            hash_list.append(line.strip())
    return hash_list


# 获取页面url列表
def get_url_list(url, hash_list):
    page_title = ''
    url_list = []
    time.sleep(1)
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
            if hashlib.sha256(url) not in hash_list:
                url_list.append(url)
    except ConnectionError:
        print('Error.')
    # print(url_list)
    return get_valid_name(str(page_title).strip()), url_list


# 获取页面上的图片地址
def get_img_by_url(url):
    # img_dict = {}
    time.sleep(1)
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
    except ConnectionError:
        print('Error.')
    return url[-10:], url_list


# 根据dict将图片保存至文件
def save_img_to_file(page_url_dict, dir_path):
    download_url_list = set()
    img_count = 0
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    for k, v in page_url_dict.items():
        target_dir = os.path.join(dir_path, k)
        # 如果文件夹已经存在，图片已经下载下来过，如果文件夹不存在则新建文件夹，爬取图片
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
            for img_url in v:
                hash_str = hashlib.sha256(img_url)
                file_name = get_name_by_url(img_url)
                time.sleep(1)
                with open(os.path.join(target_dir, file_name), 'wb') as f:
                    img_data = request.urlopen(img_url).read()
                    download_url_list.add(img_url)
                    print('img\'s length is %d' % len(img_data))
                    f.write(img_data)
                    img_count += 1
    return download_url_list


# 根据url获取文件名
def get_name_by_url(img_url):
    public_index = img_url.find('public')
    file_name = ''
    if public_index != -1:
        return get_valid_name(img_url[public_index + 7:])
    return get_valid_name(img_url[-10:])


# 去掉路径中的非法字符
def get_valid_name(name):
    invalid_char = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    return re.sub(invalid_char, "_", name)  # 替换为下划线


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
                      # 'https://www.douban.com/group/510760/?type=essence#topics',
                      # 'https://www.douban.com/group/368701/?type=essence#topics',
                      # 'https://www.douban.com/group/DQMQQ/?type=essence#topics',
                      'https://www.douban.com/group/569879/?type=essence#topics']
    hash_list = get_hash_list('hash.txt')
    download_hash_list = []
    for index_url in index_url_list:
        page_title, page_list = get_url_list(index_url, hash_list)
        page_url_dict = {}
        for url in page_list:
            result = get_img_by_url(url)
            if result is not None:
                page_url_dict[result[0]] = result[1]
        dir_path = os.path.join('E:\douban1\\', page_title)
        download_hash_list.extend(save_img_to_file(page_url_dict, dir_path))
    hash_list.extend(download_hash_list)
    hash_set = set(hash_list)
    write_hash_list_to_file(hash_set)


# 将hash列表写入文件
def write_hash_list_to_file(hash_set):
    write_str = '\n'.join(hash_set)
    with open('hash.txt', 'w') as f:
        f.write(write_str)


# 主方法
if __name__ == '__main__':
    main()
    # test_list = ['1','2','3']
    # login()
    # test_list1 = ['4','5','6']
    # print(test_list.extend(test_list1))
    # print('$'.join(test_list))
