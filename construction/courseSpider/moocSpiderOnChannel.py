import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery as pq
import re
import os
import selenium

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
    res = ''
    reference = parser.find(class_='category-content j-cover-overflow')
    for p in reference.find_all('p'):
        res = res + p.get_text() + '\n'
    return res


def get_all_introduction(parser):
    res = parser.find(class_='course-heading-intro').get_text()
    category_titles = parser.find_all(name='div', attrs={"class": re.compile('category-title')})
    category_contents = parser.find_all(name='div', attrs={"class": re.compile('category-content')})
    for ind in range(0, len(category_titles)):
        title_tag = category_titles[ind]
        content_tag = category_contents[ind]
        title = title_tag.get_text()
        content = ''
        if len(content_tag.find_all('p')) != 0:
            for p in content_tag.find_all('p'):
                content = content + p.get_text() + '\n'
        else:
            content_tag = content_tag.find_all('div')
            while len(content_tag) == 1:
                content_tag = content_tag.find_all('div')
            for item in content_tag:
                content = content + item.get_text() + '\n'
        print(title, content)
        res = res + '\n' + title + '\n' + content + '\n'
    return res

    # res = ''
    # all_intro = parser.find(id='content-section')
    # for p in all_intro.find_all('p'):
    #     res = res + p.get_text() + '\n'
    # return res

    # return parser.find(class_='content-section').get_text().replace('spContent=', '')


def get_course_title(parser):
    return parser.find(class_='course-title f-ib f-vam').get_text().replace('spContent=', '')


def get_uni_name(parser):
    return parser.find('title').get_text().split('_')[1]


def get_title(parser):
    return parser.find('title').get_text()


def get_class_info():
    try:
        parser = BeautifulSoup(chrome.page_source, 'html.parser')

        uni_name = get_uni_name(parser)
        title = get_course_title(parser)
        all_intro = get_all_introduction(parser)
        outline = get_outline(parser)
    except AttributeError:
        print('AttributeError in get_class_info')
        return

    with open(save_path + '/' + get_title(parser).replace('\n', '').replace('/', '&') + '.txt', 'w', encoding='utf-8') as f:
        f.write(uni_name + '\n')
        f.write(title + '\n')
        f.write(all_intro + '\n')
        # f.write('outline:\n' + outline)


def get_course_info_from_channel(driver):
    save_path_chl = save_path + '/'
    if not os.path.exists(save_path_chl):
        os.makedirs(save_path_chl)
    page = 1
    ind = 1
    driver.get(search_url)
    time.sleep(3)
    driver.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU ']").click()
    time.sleep(1)
    # driver.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU '][2]").click()
    # time.sleep(1)
    # driver.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU '][2]").click()
    page += 1
    while True:
        # driver.quit()
        # driver = webdriver.Chrome()

        while ind <= 20:
            time.sleep(3)
            try:
                try:
                    course = driver.find_element_by_xpath\
                                ("//div[@class='undefined']/div[@class='_1aoKr']/"
                                    "div[@class='_1gBJC']/div[@class='_2mbYw'][" + str(ind) + "]/"
                                    "div[@class='_3KiL7']/div[@class='_1Bfx4']/"
                                    "div[@class='WFpCn']")
                except selenium.common.exceptions.NoSuchElementException:
                    print('no such tag')
                    ind = ind + 1
                    continue
                time.sleep(3)
                driver.execute_script("arguments[0].click();", course)

                handles = driver.window_handles
                driver.switch_to.window(handles[-1])
                get_class_info()

                driver.get(search_url)
                for i in range(page - 1):
                    time.sleep(0.5)
                    if i == 0:
                        driver.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU ']").click()
                    else:
                        driver.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU '][2]").click()

                ind = ind + 1
            except Exception as e:
                print(e)
                print(e.__traceback__)
                print('-----------------------------------')
                continue
        if page == 1:
            next_page = driver.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU ']")
        else:
            next_page = driver.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU '][2]")

        if next_page is not None:
            time.sleep(3)
            handles_list = driver.window_handles
            for i in range(len(handles_list) - 1):
                driver.switch_to.window(handles[i])
                driver.close()
            driver.switch_to.window(handles_list[-1])

            page += 1
            next_page.click()
            ind = 1
        else:
            break


def test_xpath():
    chrome.get(search_url)
    time.sleep(4)
    chrome.find_element_by_xpath \
        ("//div[@class='undefined']/div[@class='_1aoKr']/"
         "div[@class='_1gBJC']/div[@class='_2mbYw'][" + str(10) + "]/"
         "div[@class='_3KiL7']")
    chrome.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU ']").click()
    print('click')
    time.sleep(2)
    chrome.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU '][2]").click()
    print('click')
    time.sleep(3)
    chrome.find_element_by_xpath("//div[@class='_1lKzE']/a[@class='_3YiUU '][2]").click()


if __name__ == '__main__':
    search_url = 'https://www.icourse163.org/channel/3002.htm'
    save_path = '../data/mooc/computer_channel'
    chrome = webdriver.Chrome()
    get_course_info_from_channel(chrome)
    # test_xpath()
    chrome.close()
