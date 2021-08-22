import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery as pq
import re
import os


def search_urls_of_news(driver, keywords, pageLimit, waiting):
    for keyword in keywords:
        save_path_chl = save_path + keyword + '/'
        if not os.path.exists(save_path_chl):
            os.makedirs(save_path_chl)
        driver.get(search_url + keyword)
        print(search_url + keyword)
        title_set = set()
        with open(save_path_chl + 'list.txt', 'w', encoding='utf-8') as f:
            for i in range(pageLimit):
                time.sleep(waiting)
                parser = BeautifulSoup(driver.page_source, 'html.parser')
                for news in parser.find_all(class_='news'):
                    h2 = news.find('h2')
                    source = news.find(class_='newstime').get_text().replace('spContent=', '').replace('\n', '')\
                        .replace('\t', '  ')
                    a = h2.find('a')
                    title = h2.get_text().replace('spContent=', '').replace('\n', '').replace('\t', ' ')
                    if title not in title_set:
                        print(title)
                        title_set.add(title)
                        f.write(a.get('href') + '\t' + title + '\t' + source + '\n')
                try:
                    next_page = driver.find_element_by_class_name('next')
                except selenium.common.exceptions.NoSuchElementException:
                    break
                if next_page is not None:
                    next_page.click()
                    f.flush()
                else:
                    break

                if i % 10 == 0:
                    time.sleep(waiting * 10)
                time.sleep(waiting)


def get_content_of_news(driver, keywords, waiting):
    for keyword in keywords:
        save_path_chl = save_path + keyword + '/'
        url_list = []
        with open(save_path_chl + 'list.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.split('\t'))
        for url_info in url_list:
            url, title, source = url_info
            print(url)
            driver.get(url)
            time.sleep(waiting)
            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''
            content_classes = ['p-right left', 'main-left left', 'content', 'clearfix']
            for class_ in content_classes:
                tag = parser.find(class_=class_)
                if tag is not None:
                    content = tag.get_text().replace('sp=Content', '')
                    break

            if content.replace('\n', '') is '':
                print('no content')
            try:
                with open(save_path_chl + re.sub('[<>/\\\|:*?]', '&', title) + '.txt', 'w', encoding='utf-8') as f:
                    f.write("url: " + url)
                    f.write("\ntitle: " + title)
                    f.write("\nsource: " + source)
                    f.write("\n" + content)
            except OSError:
                continue

    return


if __name__ == '__main__':
    search_url = 'http://so.news.cn/#search/0/'
    save_path = '../data/xinhua/'
    keywords = ['智能', '计算机', '电脑', '信息化']
    pageLimit = 200
    waiting = 50
    chrome = webdriver.Chrome()
    search_urls_of_news(chrome, keywords, pageLimit, waiting)
    get_content_of_news(chrome, keywords, waiting)
    chrome.close()


