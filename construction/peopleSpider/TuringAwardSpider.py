from bs4 import BeautifulSoup
import selenium
from selenium import common
from selenium import webdriver
import os
import time


def deal_get_text(string):
    return string.get_text().replace('spContent=', '').replace('\n', '').replace(' ', '')


def baikeSpider(driver):
    with open(save_path + '/list.txt', 'r', encoding='utf-8') as reader:
        for line in reader.readlines():
            url = line.split('\t')[-1]
            if len(url) < 10:
                continue
            print(url)
            driver.get(url)
            time.sleep(1.5)

            parser = BeautifulSoup(driver.page_source, 'html.parser')
            title = parser.find(class_='lemmaWgt-lemmaTitle-title').find('h1').get_text().replace('spContent=', '').replace('\n', '')\
                                .replace('\t', '  ')

            with open(save_path + '/' + title, 'w', encoding='utf-8') as writer:
                for div in parser.find_all(class_='para'):
                    content = div.get_text().replace('spContent=', '').replace('\n', '').replace(' ', '')
                    writer.write(content + '\n')


def get_urls(driver, url):
    prefix = 'https://baike.baidu.com'
    driver.get(url)
    time.sleep(1.5)
    print(url)
    parser = BeautifulSoup(driver.page_source, 'html.parser')
    with open(save_path + '/list.txt', 'w', encoding='utf-8') as writer:
        year = ''
        reason = ''
        for record in parser.find('table').find('tbody').find_all('tr'):
            infos = record.find_all('td')
            print(infos)
            if len(infos) == 2:
                writer.write(year + '\t' + deal_get_text(infos[0]) + '\t' +
                             deal_get_text(infos[1]) + '\t' + reason)
            elif len(infos) == 4:
                writer.write(deal_get_text(infos[0]) + '\t' + deal_get_text(infos[1]) + '\t' +
                             deal_get_text(infos[2]) + '\t' + deal_get_text(infos[3]))
                year = deal_get_text(infos[0])
                reason = deal_get_text(infos[3])

            if len(infos) == 2 or len(infos) == 4:
                try:
                    link_1 = infos[1].find('a').get('href')
                    if len(link_1) != 0:
                        writer.write('\t' + prefix + link_1)
                except Exception:
                    try:
                        link_2 = infos[2].find('a').get('href')
                        if len(link_2) != 0:
                            writer.write('\t' + prefix + link_2)
                    except Exception:
                        writer.write('\tnull')
                finally:
                    writer.write('\n')


if __name__ == '__main__':
    save_path = '../data/people/TuringAward'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    url = 'https://baike.baidu.com/item/图灵奖/324645?fr=aladdin'
    chrome = webdriver.Chrome()
    get_urls(chrome, url)
    baikeSpider(chrome)
    chrome.close()
