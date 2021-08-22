import requests
from bs4 import BeautifulSoup
import urllib.request
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import os


def search_urls_of_policies(driver, keywords, pageLimit):
    for keyword in keywords:
        save_path_chl = save_path + keyword + '/'
        if not os.path.exists(save_path_chl):
            os.makedirs(save_path_chl)
        driver.get(search_url + keyword)
        print(search_url + keyword)
        title_set = set()

        with open(save_path_chl + 'list.txt', 'w', encoding='utf-8') as f:
            for _ in range(pageLimit):
                time.sleep(5)
                parser = BeautifulSoup(driver.page_source, 'html.parser')
                for news in parser.find_all(class_='dys_middle_result_content_item') + \
                            parser.find_all(class_='dys_middle_result_content_item borderMarginBottomNone'):
                    source = news.find(class_='dysMiddleResultConItemRelevant clearfix').get_text().\
                        replace('spContent=', '').replace('\n', '').replace('\t', '  ')
                    a = news.find('a')
                    title = news.find('h5').get_text().replace('spContent=', '').replace('\n', '').replace('\t', ' ')
                    if title not in title_set:
                        print(title)
                        title_set.add(title)
                        f.write(a.get('href') + '\t' + title + '\t' + source + '\n')
                try:
                    next_page = driver.find_element_by_id('next')
                except selenium.common.exceptions.NoSuchElementException:
                    f.flush()
                    break
                if next_page is not None:
                    next_page.click()
                f.flush()


def get_content_of_policies(driver, keywords):
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
            content_classes = ['article oneColumn pub_border', 'pages_content', 'policyLibraryOverview_content', 'b12c']
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
    search_url = 'http://sousuo.gov.cn/s.htm?t=zhengcelibrary&q='
    save_path = '../data/gov.cn/'
    keywords = ['大数据', '软件', '网络', '智能', '计算机', '电脑', '信息化']
    pageLimit = 200
    chrome = webdriver.Chrome()
    search_urls_of_policies(chrome, keywords, pageLimit)
    get_content_of_policies(chrome, keywords)
    chrome.close()


