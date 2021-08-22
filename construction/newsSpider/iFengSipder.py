import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery as pq
import re
import os


def search_urls_of_news(driver, keywords, pageLimit):
    for keyword in keywords:
        save_path_chl = save_path + keyword + '/'
        if not os.path.exists(save_path_chl):
            os.makedirs(save_path_chl)
        driver.get(search_url + keyword)
        print(search_url + keyword)
        title_set = set()

        tag_num = 0

        with open(save_path_chl + 'list.txt', 'w', encoding='utf-8') as f:
            while True:

                parser = BeautifulSoup(driver.page_source, 'html.parser')
                pre_num = len(parser.find_all(class_='news-stream-newsStream-news-item-infor'))

                if '更多' in parser.find(class_='news-stream-newsStream-more-box').get_text():
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

                    parser = BeautifulSoup(driver.page_source, 'html.parser')
                    cur_num = len(parser.find_all(class_='news-stream-newsStream-news-item-infor'))
                    if cur_num <= pre_num and '更多' in parser.find(class_='news-stream-newsStream-more-box').get_text():
                        driver.refresh()
                        time.sleep(2)
                else:
                    break
                time.sleep(0.5)

            parser = BeautifulSoup(driver.page_source, 'html.parser')

            for news in parser.find_all(class_='news-stream-newsStream-news-item-infor'):
                h2 = news.find('h2')
                a = h2.find('a')
                title = a.get_text().replace('spContent=', '').replace('\n', '').replace('\t', ' ')
                if title not in title_set:
                    print(title)
                    title_set.add(title)
                    f.write(a.get('href') + '\t' + title + '\n')

            # for news in parser.find_all(class_='news-stream-newsStream-news-item-has-image clearfix news_item'):
            #     h2 = news.find('h2')
            #     source = news.find(class_='newstime').get_text().replace('spContent=', '').replace('\n', '')\
            #         .replace('\t', '  ')
            #     a = h2.find('a')
            #     title = h2.get_text().replace('spContent=', '').replace('\n', '').replace('\t', ' ')
            #     if title not in title_set:
            #         print(title)
            #         title_set.add(title)
            #         f.write(a.get('href') + '\t' + title + '\t' + source + '\n')
            f.flush()
            time.sleep(5)


def get_content_of_news(driver, keywords):
    for keyword in keywords:
        save_path_chl = save_path + keyword + '/'
        url_list = []
        with open(save_path_chl + 'list.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.split('\t'))
        for url_info in url_list:
            url, title = url_info
            print(url)
            driver.get(url)
            time.sleep(5)
            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''
            time_content = ''
            time_classes = ['time-1Mgp9W-1', 'timeBref-2gPzdVvm']
            content_classes = ['detailBox-2ms7ofXz', 'main_content-r5RGqegj']
            for class_ in content_classes:
                tag = parser.find(class_=class_)
                if tag is not None:
                    content = tag.get_text().replace('sp=Content', '')
                    break

            for class_ in time_classes:
                tag = parser.find(class_=class_)
                if tag is not None:
                    time_content = tag.get_text().replace('sp=Content', '')
                    break

            if content.replace('\n', '') is '':
                print('no content')

            with open(save_path_chl + re.sub('[<>/\\\|:*?]', '&', title) + '.txt', 'w', encoding='utf-8') as f:
                f.write("url: " + url)
                f.write("\ntitle: " + title)
                f.write("\nsource: " + time_content)
                f.write("\n" + content)

    return


if __name__ == '__main__':
    search_url = 'https://so.ifeng.com/?q='
    save_path = '../data/iFeng/'
    keywords = ['大数据', '软件', '网络', '智能', '计算机', '电脑', '信息化']
    pageLimit = 2
    chrome = webdriver.Chrome()
    search_urls_of_news(chrome, keywords, pageLimit)
    get_content_of_news(chrome, keywords)
    chrome.close()


