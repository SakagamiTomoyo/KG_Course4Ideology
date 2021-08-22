import requests
from bs4 import BeautifulSoup
import urllib.request
import selenium
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
        with open(save_path_chl + 'list.txt', 'w', encoding='utf-8') as f:
            for _ in range(pageLimit):
                time.sleep(10)
                parser = BeautifulSoup(driver.page_source, 'html.parser')
                for news in parser.find_all(class_='content'):
                    ttl = news.find(class_='ttl')
                    fot = news.find(class_='fot')
                    a = ttl.find('a')
                    title = ttl.get_text().replace('spContent=', '').replace('\n', '')
                    source = fot.get_text().replace('\n', '')
                    print(title)
                    f.write(a.get('href') + '\t' + title + '\t' + source + '\n')

                next_page = driver.find_element_by_class_name('page-next')
                if next_page is not None:
                    next_page.click()
                f.flush()


def get_content_of_news(driver, keywords):
    for keyword in keywords:
        save_path_chl = save_path + keyword + '/'
        url_list = []
        with open(save_path_chl + 'list.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.split('\t'))
        for url_info in url_list:
            url, title, source = url_info
            print(url)
            try:
                driver.get(url)
            except selenium.common.exceptions.WebDriverException:
                print('can not visit the url, continue')
                continue
            time.sleep(5)
            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''
            content_classes = ['rwb_zw', 'box_con', 'article scrollFlag',
                               'rm_txt_con cf', 'artDet', 'gray box_text', 'show_text']
            for class_ in content_classes:
                tag = parser.find(class_=class_)
                if tag is not None:
                    content = tag.get_text().replace('sp=Content', '')
                    break

            if content.replace('\n', '') is '':
                print('no content')
            try:
                with open(save_path_chl + title + '.txt', 'w', encoding='utf-8') as f:
                    f.write("url: " + url)
                    f.write("\ntitle: " + title)
                    f.write("\nsource: " + source)
                    f.write("\n" + content)
            except OSError:
                continue

    return


if __name__ == '__main__':
    search_url = 'http://search.people.cn/s/?keyword='
    save_path = '../data/people.cn/'
    keywords = ['大数据', '软件', '网络', '智能', '计算机', '电脑', '信息化']
    pageLimit = 200
    chrome = webdriver.Chrome()
    # search_urls_of_news(chrome, keywords, pageLimit)
    get_content_of_news(chrome, keywords)
    chrome.close()


