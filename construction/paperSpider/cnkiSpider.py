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
import random
import urllib

def deal_get_text(string):
    return string.get_text().replace('spContent=', '').replace('\n', '').replace(' ', '').strip()


def search_urls_of_news(driver, keywords, prefix_word, pageLimit, waiting):
    for keyword in keywords:
        save_path_chl = save_path + keyword + '/'
        if not os.path.exists(save_path_chl):
            os.makedirs(save_path_chl)
        driver.get(search_url)
        time.sleep(1)

        driver.find_element_by_id('txt_search').send_keys(prefix_word + ' ' + keyword)
        time.sleep(1)
        driver.find_element_by_class_name('search-btn').click()
        time.sleep(1)

        title_set = set()
        with open(save_path_chl + 'list.txt', 'w', encoding='utf-8') as f:
            for i in range(pageLimit):
                new_record = False

                parser = BeautifulSoup(driver.page_source, 'html.parser')
                for paper in parser.find(class_='result-table-list').find('tbody').find_all('tr'):
                    time.sleep(random.randint(1, waiting / 2))
                    name = paper.find(class_='name')
                    title = deal_get_text(name)
                    authors = deal_get_text(paper.find(class_='author'))
                    source = deal_get_text(paper.find(class_='source'))
                    date = deal_get_text(paper.find(class_='date'))

                    kk = re.compile(r'FileName=(.*?)&DbName=(.*?)&DbCode=(.*?)&')
                    infos = kk.findall(name.find('a').get('href'))
                    infos = [infos[0][0], infos[0][1], infos[0][2]]
                    # print(infos, type(infos))
                    url = prefix_url + 'kcms/detail/detail.aspx?Filename=' + str(infos[0])\
                          + '&DbName=' + str(infos[1])\
                          + '&DbCode=' + str(infos[2])

                    print(title)
                    print(url)

                    if title not in title_set:
                        title_set.add(title)
                        new_record = True
                        f.write(title + '\t' + authors + '\t' + source + '\t' + date + '\t' + url + '\n')
                next_page = None

                if not new_record:
                    break

                try:
                    next_page = driver.find_element_by_id('PageNext')
                    if next_page is not None:
                        next_page.send_keys(Keys.ARROW_RIGHT)
                        f.flush()
                        time.sleep(random.randint(waiting / 2, waiting * 2))
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
                url_list.append(line.replace('\n', '').split('\t'))
        for url_info in url_list:
            title, author, source, date, url = url_info
            print(url)
            try:
                time.sleep(random.randint(int(waiting / 2), waiting))
                driver.get(url)
            except selenium.common.exceptions.WebDriverException:
                print('can not open url of paper information')
                continue

            time.sleep(2)
            try:
                driver.find_element_by_class_name('btn-html').click()
                handles = driver.window_handles
                driver.switch_to.window(handles[-1])
            except selenium.common.exceptions.ElementNotInteractableException:
                continue

            # parser = BeautifulSoup(driver.page_source, 'html.parser')

            # href = parser.find(class_='btn-html').find('a').get('href')
            # print(href)
            # try:
            #     time.sleep(random.randint(int(waiting / 2), waiting))
            #     driver.get(href)
            # except selenium.common.exceptions.WebDriverException:
            #     print('can not open url of paper content')
            #     continue

            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''

            if parser.find(class_='c_verify-box') is not None:
                time.sleep(10)
                parser = BeautifulSoup(driver.page_source, 'html.parser')

            try:
                count = 0
                path_name = save_path_chl + re.sub('[<>/\\\|:*?"]', '&', title)
                if not os.path.exists(path_name):
                    os.makedirs(path_name)

                for tag in parser.find(class_='content').descendants:
                    try:
                        class_name = tag.get('class')
                        if class_name[0] in ['data', 'anchor-tag', 'p1', 'reference']:
                            content += deal_get_text(tag) + '\n'
                            print(deal_get_text(tag))
                        if class_name[0] in ['area_img']:
                            print('pic' + str(count))
                            urllib.request.urlretrieve(
                                img_prefix_url + tag.find('a').get('href'), path_name + '/' +
                                                                            str(count + 1) + ' ' + deal_get_text(tag) + '.jpg')
                            count = count + 1
                    except AttributeError:
                        continue
                    except TypeError:
                        continue

                with open(path_name + '/' + 'content.txt', 'w', encoding='utf-8') as f:
                    f.write(content)

            except OSError:
                continue
            except AttributeError:
                continue

            time.sleep(random.randint(int(waiting / 2), waiting))

            handles_list = driver.window_handles
            for i in range(len(handles_list) - 1):
                driver.switch_to.window(handles[i])
                driver.close()
            driver.switch_to.window(handles_list[-1])

    return


def get_paper_test(driver):
    save_path_chl = save_path + '计算机' + '/'
    parser = None
    driver.get()

    try:
        count = 0
        path_name = save_path_chl + re.sub('[<>/\\\|:*?"]', '&', title)
        if os.path.exists(path_name):
            os.makedirs(path_name)

        for tag in parser.find(class_='content').descendants:
            try:
                class_name = tag.get('class')
            except AttributeError:
                continue
            if class_name in ['data', 'anchor-tag', 'p1']:
                print(deal_get_text(tag))
            if class_name in ['area_img']:
                print(count)
                urllib.request.urlretrieve(
                    img_prefix_url + tag.find('a').get('href'), path_name + str(count) + '.jpg')

        with open(path_name + '.txt', 'w', encoding='utf-8') as f:
            pass

    except OSError:
        return


if __name__ == '__main__':
    # kk = re.compile(r'FileName=(.*?)&DbName=(.*?)&DbCode=(.*?)&')
    # print(kk.findall(
    #     'KNS8/Detailsfield=fn&QueryID=0&CurRec=1&recid=&FileName=XXWX2021031700R&DbName=CAPJLAST&DbCode=CAPJ&yx=Y&pr=&URLID=21.1106.TP.20210319.1034.020'))
    prefix_url = 'https://kns.cnki.net/'
    img_prefix_url = 'https://kns.cnki.net/KXReader/'
    search_url = 'https://kns.cnki.net/kns8/defaultresult/index'
    save_path = '../data/cnki/'
    prefix_word = '思政'
    keywords = [
        # '计算机',
        # '人工智能',
        # '互联网',
        '大数据'
    ]
    pageLimit = 200
    waiting = 20
    chrome = webdriver.Chrome()
    # search_urls_of_news(chrome, keywords, prefix_word, pageLimit, waiting)
    get_content_of_news(chrome, keywords, waiting)
    chrome.close()
