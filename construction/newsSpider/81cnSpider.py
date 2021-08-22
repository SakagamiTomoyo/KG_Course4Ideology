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
                for news in parser.find(id='DETAILELE1').find_all('table'):
                    a = news.find('tbody').find('tr').find('td').find('a')
                    title = a.get_text().replace('spContent=', '').replace('\n', '')\
                        .replace('\t', '  ')
                    url = a.get('href')
                    time_stamp = news.find('tbody').find_all('tr')[-1].find('td').get_text().replace('spContent=', '')\
                        .replace('\n', '').replace('\t', '  ').split('\xa0\xa0')[-2][:-2]
                    if title not in title_set:
                        print(title)
                        title_set.add(title)
                        f.write(title + '\t' + url + '\t' + time_stamp + '\n')

                next_page = None

                try:
                    next_pages = driver.find_elements_by_xpath("//div[@class='scott']/a")
                    for item in next_pages:
                        if str(i + 2) in item.get_attribute('textContent'):
                            next_page = item
                    if next_page is not None:
                        next_page.click()
                        f.flush()
                    else:
                        break
                except selenium.common.exceptions.NoSuchElementException:
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
            except selenium.common.exceptions.WebDriverException:
                continue
            time.sleep(waiting)
            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''
            content_classes = ['content']
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
    search_url = 'http://search.chinamil.com.cn/search/milsearch/stouch.jsp?searchfield=TITLE&indexsearch=1&keyword='
    save_path = '../data/81cn/'
    keywords = ['大数据', '软件', '网络', '智能', '计算机', '电脑', '信息化']
    pageLimit = 200
    waiting = 10
    chrome = webdriver.Chrome()
    # search_urls_of_news(chrome, keywords, pageLimit, waiting)
    get_content_of_news(chrome, keywords, waiting)
    chrome.close()


