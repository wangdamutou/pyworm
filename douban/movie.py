import re
from urllib import request
from bs4 import BeautifulSoup as bs
import jieba
import numpy
import codecs
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def get_now_playing_movie_list():
    resp = request.urlopen('https://movie.douban.com/cinema/nowplaying/changsha/')
    html_data = resp.read().decode('utf-8')

    # 使用BeautifulSoup库进行html代码解析
    soup = bs(html_data, 'html.parser')
    # 获取id为nowplaying的div
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    # 获取class为list-item的列表
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')

    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
    return nowplaying_list


# 获取影评
def get_comments(movie_id, page_num):
    # url = 'https://movie.douban.com/subject/' + movieId + '/comments?status=P'
    if page_num > 0:
        start = (page_num - 1) * 20
    else:
        return False
    url = ('https://movie.douban.com/subject/' + movie_id + '/comments?start=' +
           str(start) + '&limit=20&sort=new_score&status=P')
    resp = request.urlopen(url)
    html_data = resp.read().decode('utf-8')

    # 使用BeautifulSoup库进行html代码解析
    soup = bs(html_data, 'html.parser')
    # 获取id为comment的div
    comment_div_list = soup.find_all('div', id='comments')
    # 获取class为comment-item的列表
    comment_item_list = comment_div_list[0].find_all('div', class_='comment-item')
    comment_list = []
    for item in comment_item_list:
        # comment_dict = {}
        comment = item.find_all('span', class_='short')[0].get_text()
        if comment is not None:
            # comment_dict['comment'] = comment
            comment_list.append(comment)
        # 后续添加评分
        # comment_list.append(comment_dict)
    print(comment_list)
    return comment_list


def main():
    comments = []
    now_playing_movie_list = get_now_playing_movie_list()
    for i in range(10):
        num = i + 1
        comments.append(get_comments(now_playing_movie_list[4]['id'], num))
    print(now_playing_movie_list[4]['name'])
    comment_str = ''
    # 将列表中的数据转换为字符串
    for k in range(len(comments)):
        comment_str = comment_str + (str(comments[k])).strip()
    # 使用正则表达式去除标点
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filter_data = re.findall(pattern, comment_str)
    cleaned_comments = ''.join(filter_data)

    # 使用结巴分词进行中文分词
    segment = jieba.lcut(cleaned_comments)
    words_df = pd.DataFrame({'segment': segment})

    # 去掉停用词
    stop_words = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                             encoding='GBK')
    words_df = words_df[~words_df.segment.isin(stop_words.stopword)]

    # 统计词频
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"count": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["count"], ascending=False)

    # 用词云进行显示
    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80)
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}

    # word_frequence_list = []
    # for key in word_frequence:
    #     temp = (key, word_frequence[key])
    #     word_frequence_list.append(temp)

    wordcloud = wordcloud.fit_words(word_frequence)
    plt.imshow(wordcloud)
    plt.savefig("result.jpg")

# 主函数
main()
