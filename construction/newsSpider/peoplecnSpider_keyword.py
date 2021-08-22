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


def search_urls_of_news(driver, keywords_id, pageLimit, threshold):
    for id, keyword in keywords_id.items():
        title_set = set()
        save_path_chl = save_path + str(id) + '/'
        if not os.path.exists(save_path_chl):
            os.makedirs(save_path_chl)
        driver.get(search_url + keyword.replace('\t', ' '))
        with open(save_path_chl + 'list.txt', 'w', encoding='utf-8') as f:
            for _ in range(pageLimit):
                time.sleep(3)
                parser = BeautifulSoup(driver.page_source, 'html.parser')
                for news in parser.find_all(class_='content'):
                    ttl = news.find(class_='ttl')
                    fot = news.find(class_='fot')
                    abs = news.find(class_='abs')

                    a = ttl.find('a')
                    title = ttl.get_text().replace('spContent=', '').replace('\n', '')
                    source = fot.get_text().replace('\n', '')

                    word_set = {}

                    for word in ttl.find_all('em'):
                        word = word.get_text().replace('spContent=', '').replace('\n', '')
                        if word not in word_set.keys():
                            word_set[word] = 1
                        else:
                            word_set[word] += 1

                    for word in abs.find_all('em'):
                        word = word.get_text().replace('spContent=', '').replace('\n', '')
                        if word not in word_set.keys():
                            word_set[word] = 1
                        else:
                            word_set[word] += 1

                    print(keyword.split('\t'))
                    try:
                        section, chapter, course = keyword.split('\t')
                    except Exception:
                        continue
                    max_score = len(section) + len(chapter) + len(course)
                    score = 0

                    for word, count in word_set.items():
                        # print(type(word), type(section))

                        if word in section or section in word:
                            # for i in range(1, count + 1):
                            #     score += 2 * len(word) / i
                            score += 1 * len(word)
                        elif word in chapter or chapter in word:
                            # for i in range(1, count + 1):
                            #     score += 1.5 * len(word) / i
                            score += 1 * len(word)
                        elif word in course or course in word:
                            # for i in range(1, count + 1):
                            #     score += 1 * len(word) / i
                            score += 1 * len(word)
                    print(title, word_set, float(score) / max_score)

                    if score > threshold * max_score:
                        if title.strip() not in title_set:
                            title_set.add(title.strip())
                            f.write(a.get('href') + '\t' + title + '\t' + source + '\n')

                try:
                    next_page = driver.find_element_by_class_name('page-next')
                    if next_page is not None:
                        next_page.click()
                    f.flush()
                except Exception:
                    continue


def get_content_of_news(driver, keywords_id):
    for id, keyword in keywords_id.items():
        save_path_chl = save_path + str(id) + '/'
        url_list = []
        with open(save_path_chl + 'list.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.split('\t'))
        for url_info in url_list:
            url, title, source = url_info
            print(url)
            try:
                driver.get(url)
            except selenium.common.exceptions.WebDriverException:
                print('can not visit the url, continue')
                continue
            time.sleep(3)
            parser = BeautifulSoup(driver.page_source, 'html.parser')
            content = ''
            content_classes = ['rwb_zw', 'box_con', 'article scrollFlag',
                               'rm_txt_con cf', 'artDet', 'gray box_text', 'show_text']
            for class_ in content_classes:
                tag = parser.find(class_=class_)
                if tag is not None:
                    content = tag.get_text().replace('sp=Content', '')
                    break

            if content.replace('\n', '') is '':
                print('no content')
            try:
                with open(save_path_chl + title + '.txt', 'w', encoding='utf-8') as f:
                    f.write("url: " + url)
                    f.write("\ntitle: " + title)
                    f.write("\nsource: " + source)
                    f.write("\n" + content)
            except OSError:
                continue

    return


def get_keywords():
    res = []
    res_dict = {}
    with open(entity_path + 'courses.txt', 'r', encoding='utf-8') as course_reader:
        for course in course_reader.readlines():
            course_id, course_name = course.split('\t')[0], course.split('\t')[1].replace('\n', '')
            with open(entity_path + 'chapters.txt', 'r', encoding='utf-8') as chapter_reader:
                for chapter in chapter_reader.readlines():
                    chapter_course, chapter_id, chapter_name = chapter.split('\t')
                    if int(chapter_course) != int(course_id):
                        continue
                    with open(entity_path + 'sections.txt', 'r', encoding='utf-8') as section_reader:
                        for section in section_reader.readlines():
                            # print(section)
                            section_chapter, section_id, section_name = section.split('\t')
                            if int(section_chapter) != int(chapter_id):
                                continue
                            search_word = section_name.replace('\n', '') + '\t' + chapter_name.replace('\n', '') + '\t' + \
                                          course_name.replace('\n', '')

                            search_word = re.sub('第.*((单元)|周|篇|讲|章)', '', search_word)
                            search_word = re.sub('_|\d+|(hms)|(ms)|(ii)|(上)|(下)|(中)|(（上）)|(（中）)|(（下）)', '', search_word)
                            search_word = re.sub('[.、（）]', ' ', search_word)
                            search_word = search_word.replace('-', ' ')
                            # print(search_word)

                            if int(section_id) > 1086:
                                res.append(search_word)
                                res_dict[section_id] = search_word
    return res, res_dict


if __name__ == '__main__':
    search_url = 'http://search.people.cn/s/?keyword='
    save_path = '../data/people.cn/'
    entity_path = '../data/entities/'
    keywords, keywords_id = get_keywords()
    pageLimit = 3
    threshold = 0.15
    chrome = webdriver.Chrome()
    search_urls_of_news(chrome, keywords_id, pageLimit, threshold)
    get_content_of_news(chrome, keywords_id)
    chrome.close()
