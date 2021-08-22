import re
import requests
import jieba
import jieba.posseg as posseg
from bs4 import BeautifulSoup
import urllib.request
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import os


def deal_get_text(string):
    return string.get_text().replace('spContent=', '').replace('\n', '').replace(' ', '')


def baikeSpider(things_save_path, driver):

    for dir in os.listdir(things_save_path):
        for file in os.listdir(things_save_path + dir):
            # print(dir, file)
            # print(things_save_path + dir + '/' + file)
            if 'list.txt' not in file and 'people' not in file:
                file_path = things_save_path + dir + '/' + file
                save_path = things_save_path + dir + '/people/'

                # print(file_path)
                people_name = ''
                with open(file_path, 'r', encoding='utf-8') as reader:
                    people_name = reader.readline().replace('\n', '')
                # print(people_name)

                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                if people_name == 'null':
                    continue
                else:
                    people_name = re.split('[、;，]', people_name)
                    for people in people_name:
                        if len(people) == 0:
                            continue
                        else:
                            people = re.sub('[<>/\\\|:*?"]', '&', people)
                            print(people)
                            with open(save_path + people + '.txt', 'w', encoding='utf-8') as writer:

                                driver.get('https://baike.baidu.com/item/' + people)
                                time.sleep(1.5)
                                parser = BeautifulSoup(driver.page_source, 'html.parser')

                                people_info = file + '\n'

                                try:
                                    writer.write(people_info)
                                    print(people_info)
                                    for div in parser.find_all(class_='para'):

                                        content = div.get_text().replace('spContent=', '').replace('\n', '').replace(' ', '')
                                        print(content)
                                        writer.write(content + '\n')
                                except Exception as e:
                                    print(e)
                                    continue


def test():
    for dir in os.listdir(things_save_path):
        for file in os.listdir(things_save_path + dir):
            print(dir, file)
            print(things_save_path + dir + '/' + file)

if __name__ == '__main__':
    entity_path = '../data/entities/'
    baidu_prefix = 'https://www.baidu.com/s?ie=UTF-8&wd='
    baike_prefix = 'https://baike.baidu.com/search/none?pn=0&rn=10&enc=utf8&word='
    baike_item_prefix = 'https://baike.baidu.com'
    things_save_path = '../data/things/'
    people_save_path = '../data/people/'
    baidu_suffix = ' 百度百科'
    chrome = webdriver.Chrome()
    baikeSpider(things_save_path, chrome)
    chrome.close()
