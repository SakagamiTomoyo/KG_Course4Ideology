import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery as pq
import re


def get_university_url():
    chrome.get(all_universities_URL)
    parser = BeautifulSoup(chrome.page_source, 'html.parser')
    universities_url_dict = {}

    print('get urls of universities')
    for university_div in parser.find_all('a', class_='u-usity f-fl'):
        img = university_div.find('img')
        with open('../data/universities_of_mooc', 'a', encoding='utf-8') as f:
            f.write(university_div.get('href') + '\t' + img['alt'] + '\n')
        universities_url_dict[img['alt']] = university_div.get('href')
    print('urls of universities are ready')

    return universities_url_dict


def get_foreword(parser):
    return parser.find('div', class_='f-dn').get_text()


def get_intro(parser):
    return parser.find(class_='f-richEditorText').get_text()


def get_outline(parser):
    res = ''
    outline = parser.find(class_='outline')
    for p in outline.find_all('p'):
        res = res + p.get_text() + '\n'
    return res


def get_reference(parser):
    return


def get_all_introduction(parser):
    return parser.find(id='content-section').get_text().replace('spContent=', '')


def get_course_title(parser):
    return parser.find(class_='course-title f-ib f-vam').get_text().replace('spContent=', '')


def get_uni_name(parser):
    return parser.find('title').get_text().split('_')[1]


def get_title(parser):
    return parser.find('title').get_text()


def get_class_info(course_url):
    try:
        chrome.get(course_url)
        time.sleep(3)

        parser = BeautifulSoup(chrome.page_source, 'html.parser')

        uni_name = get_uni_name(parser)
        title = get_course_title(parser)
        all_intro = get_all_introduction(parser)
    except AttributeError:
        print('AttributeError in get_class_info')
        return

    with open('../data/mooc/' + get_title(parser).replace('\n', '').replace('/', '&') + '.txt', 'w', encoding='utf-8') as f:
        f.write(uni_name + '\n')
        f.write(title + '\n')
        f.write(all_intro + '\n')
        f.write('outline:\n' + get_outline(parser))


def get_course_urls(pageSource, filter=None):
    res = []
    parser = BeautifulSoup(pageSource, 'html.parser')
    for div in parser.find_all(class_='u-clist f-bgw f-cb f-pr j-href ga-click'):
        url = mooc_URL[:-1] + div.get('data-href')
        if 'packages' in url:
            continue
        if 'university' in filter:
            if 'undefined' not in url:
                res.append(url)
        else:
            res.append(url)
    return res


def class_course_urls(keywords, course_tag=False):
    def quote(x):
        return urllib.parse.quote(x)

    keywords = list(map(quote, keywords))
    url_dict = {}
    for kws in keywords:
        url_dict[kws] = search_URL + kws
    return url_dict


def get_class_info_from_search(search_urls):
    class_urls = []

    for keyword, url in search_urls.items():
        chrome.get(url)
        time.sleep(3)
        data = chrome.page_source
        course_urls = get_course_urls(data, filter=['university'])
        if any(course_urls):
            [class_urls.append(i) for i in course_urls]

    class_urls = list(set(class_urls))
    return class_urls


if __name__ == "__main__":
    all_universities_URL = 'https://www.icourse163.org/university/view/all.htm#/'
    mooc_URL = 'https://www.icourse163.org/'
    course_URL = 'http://www.icourse163.org/course/'
    search_URL = "http://www.icourse163.org/search.htm?search="
    keywords = ['计算机', '人工智能', '机器学习', '网络安全',
                '深度学习', '编译', '软件', '操作系统',
                '数据', '算法', 'c', '系统结构', '体系结构',
                'c++', 'python', 'java', '云计算',
                '面向对象', '计算机网络', 'linux', '图形学']
    # keywords = ['计算机系统结构']
    course_tag = True
    chrome = webdriver.Chrome()

    search_urls = class_course_urls(keywords, course_tag)
    course_urls = get_class_info_from_search(search_urls)
    for course_url in course_urls:
        get_class_info(course_url)

    chrome.close()
