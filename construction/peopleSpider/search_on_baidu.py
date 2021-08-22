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


def baikeSpider(save_path, keyword_id, driver):
    for id, keyword in keyword_id.items():
        with open(save_path + str(id) + '/list.txt', 'r', encoding='utf-8') as reader:
            for line in reader.readlines():

                people_info = ''
                flag = True

                url = line.split('\t')[0]
                if len(url) < 10:
                    continue
                # print(url)
                driver.get(url)
                time.sleep(1.5)

                parser = BeautifulSoup(driver.page_source, 'html.parser')

                try:
                    dts = parser.find(class_='basic-info cmn-clearfix').find_all('dt')
                    dds = parser.find(class_='basic-info cmn-clearfix').find_all('dd')

                    for i in range(len(dts)):
                        record = deal_get_text(dts[i])
                        if '人' in record or '者' in record or '企业' in record:
                            people_info = deal_get_text(dds[i]) + ';'
                            print(people_info)
                            flag = False
                    if flag:
                        people_info = 'null'
                except Exception:
                    people_info = 'null'
                finally:
                    people_info += '\n'

                try:
                    title = parser.find(class_='lemmaWgt-lemmaTitle-title').find('h1').get_text().\
                        replace('spContent=', '').replace('\n', '').replace('\t', '  ')
                    with open(save_path + str(id) + '/' + title, 'w', encoding='utf-8') as writer:
                        writer.write(people_info)
                        for div in parser.find_all(class_='para'):
                            content = div.get_text().replace('spContent=', '').replace('\n', '').replace(' ', '')
                            writer.write(content + '\n')
                except Exception:
                    continue


def get_keywords():
    res = []
    res_dict = {}
    with open(entity_path + 'sections.txt', 'r', encoding='utf-8') as section_reader:
        for section in section_reader.readlines():
            if '导学' in section \
                    or '讨论' in section \
                    or '总结' in section \
                    or '作业' in section \
                    or '循序渐进' in section :
                continue
            ection_chapter, section_id, section_name = section.split('\t')
            search_word = section_name.replace('\n', '')
            search_word = re.sub('第.*((单元)|周|篇|讲|章)', '', search_word)
            search_word = re.sub('_|\d+|(hms)|(ms)|(ii)|(上)|(下)|(中)|(（上）)|(（中）)|(（下）)', '', search_word)
            search_word = re.sub('[.、（）：]', ' ', search_word)
            search_word = search_word.replace('-', ' ').replace('()', '')
            search_word = search_word.strip()
            res.append(search_word)
            # print(search_word)
            # if int(section_id) < 200 or int(section_id) > 300:
            #     continue
            res_dict[section_id] = [search_word, jieba.posseg.lcut(search_word)]
    return res, res_dict


def search_on_baidu(driver, keywords_id):
    for id, keyword in keywords_id.items():
        title_set = set()
        save_path_chl = things_save_path + str(id) + '/'
        if not os.path.exists(save_path_chl):
            os.makedirs(save_path_chl)
        with open(save_path_chl + 'list.txt', 'w', encoding='utf-8') as writer:
            url_list = [baike_prefix + keyword[0]]
            eng_keyword = []
            n_keyword = []
            for word_pair in keyword[1]:
                if 'eng' in word_pair.flag:
                    eng_keyword.append(word_pair.word)
                elif 'n' in word_pair.flag:
                    n_keyword.append(word_pair.word)
            url_list.append(baike_prefix + ' '.join(eng_keyword))
            url_list.append(baike_prefix + ' '.join(n_keyword))
            for url in url_list:
                print(url)
                driver.get(url)
                time.sleep(3)
                parser = BeautifulSoup(driver.page_source, 'html.parser')
                if 'wiki-search' in parser.find('body').attrs['class']:
                    try:
                        for dd in parser.find(class_='search-list').find_all('dd'):
                            url = dd.find('a').get('href')
                            if 'http' not in url:
                                url = baike_item_prefix + url
                            title = deal_get_text(dd.find('a'))
                            if title not in title_set:
                                title_set.add(title)
                                writer.write(url + '\t' + title + '\n')
                    except AttributeError as e:
                        print(e)
                        continue
                else:
                    writer.write(url + '\t' + parser.find(class_='lemmaWgt-lemmaTitle-title').find('h1').
                                 get_text().replace('spContent=', '').replace('\n', '').replace('\t', '  ') + '\n')


if __name__ == '__main__':
    entity_path = '../data/entities/'
    baidu_prefix = 'https://www.baidu.com/s?ie=UTF-8&wd='
    baike_prefix = 'https://baike.baidu.com/search/none?pn=0&rn=10&enc=utf8&word='
    baike_item_prefix = 'https://baike.baidu.com'
    things_save_path = '../data/things/'
    people_save_path = '../data/people/'
    baidu_suffix = ' 百度百科'
    chrome = webdriver.Chrome()
    keywords, keywords_id = get_keywords()
    # search_on_baidu(chrome, keywords_id)
    baikeSpider(things_save_path, keywords_id, chrome)
    chrome.close()
