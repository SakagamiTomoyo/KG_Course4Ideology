import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
                for news in parser.find_all(class_='news_item'):
                    title_tag = news.find(class_='news_title')
                    if title_tag is None:
                        publish_time = news.find(class_='news_other').get_text().replace('spContent=', '')\
                            .replace('\n', '').replace('\t', '  ')
                        f.write(publish_time.strip().split(' ')[-2] + ' '
                                + publish_time.strip().split(' ')[-1] + '\n')
                        continue
                    title = title_tag.get_text().replace('spContent=', '').replace('\n', '')\
                        .replace('\t', '  ')
                    url = news.find('a').get('href')

                    if title not in title_set:
                        print(title)
                        title_set.add(title)
                        f.write(title + '\t' + url + '\t')

                next_pages = driver.find_elements_by_xpath("//div[@id='pagediv']/a")
                next_page = None
                for item in next_pages:
                    # print(item.get_attribute('textContent'))
                    if '下一页' in item.get_attribute('textContent'):
                        next_page = item
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
            try:
                title, url, time_stamp = url_info
            except ValueError:
                print('valueError')
                continue
            print(url)
            driver.get(url)
            time.sleep(5)
            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''
            content_classes = ['content', 'content_desc']
            for class_ in content_classes:
                tag = parser.find(class_=class_)
                if tag is not None:
                    content = tag.get_text().replace('sp=Content', '')
                    break

            if content.replace('\n', '') is '':
                print('no content')
            try:
                with open(save_path_chl + re.sub('[<>/\\\|:*?"]', '&', title) + '.txt', 'w', encoding='utf-8') as f:
                    f.write("url: " + url)
                    f.write("\ntitle: " + title)
                    f.write("\ntime: " + time_stamp)
                    f.write("\n" + content)
            except OSError:
                continue

    return


if __name__ == '__main__':
    search_url = 'http://sou.chinanews.com/search.do?q='
    save_path = '../data/Chinanews/'
    keywords = ['大数据', '软件', '网络', '智能', '计算机', '电脑', '信息化']
    pageLimit = 200
    chrome = webdriver.Chrome()
    # search_urls_of_news(chrome, keywords, pageLimit)
    get_content_of_news(chrome, keywords)
    chrome.close()


