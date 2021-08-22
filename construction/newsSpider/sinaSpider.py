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
        with open(save_path_chl + 'list.txt', 'w', encoding='utf-8') as f:
            for _ in range(pageLimit):
                time.sleep(10)
                parser = BeautifulSoup(driver.page_source, 'html.parser')
                for news in parser.find_all(class_='box-result clearfix'):
                    h2 = news.find('h2')
                    source = h2.find('span').get_text().replace('spContent=', '').replace('\n', '').replace('\t', ' ')
                    a = h2.find('a')
                    title = a.get_text().replace('spContent=', '').replace('\n', '').replace('\t', ' ')
                    if title not in title_set:
                        print(title)
                        title_set.add(title)
                        f.write(a.get('href') + '\t' + title + '\t' + source + '\n')

                next_pages = driver.find_elements_by_xpath("//div[@class='pagebox']/a")
                next_page = None
                for item in next_pages:
                    if '下一页' in item.get_attribute('textContent'):
                        next_page = item
                if next_page is not None:
                    next_page.click()
                    f.flush()
                else:
                    break


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
            driver.get(url)
            time.sleep(5)
            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''
            content_classes = ['article', 'article-content-left', 'article-body main-body']
            for class_ in content_classes:
                tag = parser.find(class_=class_)
                if tag is not None:
                    if tag.find('p') is not None:
                        for p in tag.find_all('p'):
                            content = content + p.get_text().replace('sp=Content', '') + '\n'
                    else:
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
    search_url = 'https://search.sina.com.cn/?c=news&from=channel&ie=utf-8&q='
    save_path = '../data/sina/'
    keywords = ['大数据', '软件', '网络', '智能', '计算机', '电脑', '信息化']
    pageLimit = 200
    chrome = webdriver.Chrome()
    search_urls_of_news(chrome, keywords, pageLimit)
    get_content_of_news(chrome, keywords)
    chrome.close()


