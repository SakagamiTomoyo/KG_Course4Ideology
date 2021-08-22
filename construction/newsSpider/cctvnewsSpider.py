import requests
from bs4 import BeautifulSoup
import urllib.request
import selenium
from selenium import common
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
                for news in parser.find(class_='outer').find('ul').find_all('li'):
                    a = news.find(class_='tit').find('span').find('a')
                    title = a.get_text().replace('spContent=', '').replace('\n', '')\
                        .replace('\t', '  ')
                    url = a.get('href')
                    time_stamp = news.find(class_='tim').get_text().replace('spContent=', '')\
                        .replace('\n', '').replace('\t', '  ')
                    if title not in title_set:
                        print(title)
                        title_set.add(title)
                        f.write(title + '\t' + url[url.index('https'): url.index('shtml') + 5] + '\t' + time_stamp + '\n')

                try:
                    next_page = driver.find_element_by_class_name('page-next')
                    if next_page is not None:
                        next_page.click()
                        f.flush()
                    else:
                        break
                except selenium.common.exceptions.NoSuchElementException:
                    break
                except Exception:
                    break



def get_content_of_news(driver, keywords, waiting):
    for keyword in keywords:
        save_path_chl = save_path + keyword + '/'
        url_list = []
        with open(save_path_chl + 'list.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.split('\t'))
        for url_info in url_list:
            title, url, time_stamp = url_info
            print(url)
            try:
                driver.get(url)
            except Exception:
                print('error')
                continue
            time.sleep(waiting)
            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''
            content_classes = ['cnt_bd', 'content_area']
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
    search_url = 'https://search.cctv.com/search.php?type=web&qtext='
    save_path = '../data/cctvnews/'
    keywords = ['大数据', '软件', '网络', '智能', '计算机', '电脑', '信息化']
    pageLimit = 200
    waiting = 10
    chrome = webdriver.Chrome()
    search_urls_of_news(chrome, keywords, pageLimit, waiting)
    get_content_of_news(chrome, keywords, waiting)
    chrome.close()


