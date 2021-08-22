# 爬取mooc课程信息实战

import urllib.parse  # 后面将要搜索的关键字转换为url形式会用到
import time  # 用模拟浏览器操作时，每次点击下一页需要停顿5秒，会用到
import random  # ip ua
from selenium import webdriver  # 模拟浏览器
from pyquery import PyQuery as pq  # 匹配
import re  # 正则表达式需要用到

# 系列课程网址的前缀
startUrl = "http://www.icourse163.org/search.htm?search="
# 要搜索的关键字
keywds = ['计算机编程教育基础', 'c++入门知识']

'''
作用：用来根据关键字构造某系列课程的网址
参数：keywords是一个关键字列表
返回值：返回所有系列课程的首页网址
'''


def class_course_urls(keywords):
    # 将关键字转换成URL编码
    def quote(x):
        return urllib.parse.quote(x)

    keywords = list(map(quote, keywords))
    # 构造每一系列课程的网址
    urls = []
    for kws in keywords:
        urls.append(startUrl + kws)
    return urls


'''
作用：获取某系列课程中一页的所有课程的网址
参数：pageSource某页的源码
返回值：返回爬取系列课程中一页的所有课程的网址
'''


def get_course_urls(pageSource):
    # 爬取系列课程中一页的所有课程的网址
    code = pq(pageSource)
    href = code("#j-courseCardListBox a")
    urlList = []
    # 去除掉不是课程网址的信息，即去掉不含www和含https的网址
    for i in href:
        temp = "http:" + str(code(i).attr("href"))
        if temp.__contains__("www") and temp.__contains__("course") and ("-" in temp):
            urlList.append(temp)
    # 去除重复的url地址
    urlList = list(set(urlList))
    return urlList


'''
作用：对某一系列课程进行翻页爬取该系列课程的所有课程的网址
参数：class_urls是某系列课程的首页网址
返回值：该系列课程所有课程的网址
'''


def get_class_course_urls(class_url):
    # 打开模拟浏览器
    chrome = webdriver.PhantomJS()
    # 爬取该系列课程的首页
    chrome.get(class_url)

    allUrl = []  # 用来存放该系列课程的所有课程的网址
    count = 1  # 用来标记当前正在爬取第几页
    while (True):
        try:
            # 用来判断是否是到最后一页的素材
            data = chrome.page_source
            pat = '<a class="th-bk-disable-gh">(.*?)</a>'

            print('正在爬取第', count, '页...')  # 打印正在爬取的页码
            # 调用get_course_urls()函数，将这一页的所有课程的网址添加到allUrl中
            [allUrl.append(i) for i in get_course_urls(data)]

            # 判断是否爬到最后一页
            d = re.compile(pat).findall(data)
            if d != [] and count != 1:
                # 将最后一页爬取到的课程网址添加到allUrl中
                # [allUrl.append(i) for i in get_course_urls(chrome.page_source)]
                # print('正在爬取第', count+1, '页...')
                break  # 爬到最后一页，跳出循环
            # 若没有爬到最后一页，就用模拟浏览器模拟人点击‘下一页’
            chrome.find_element_by_link_text("下一页").click()
            time.sleep(5)  # 停顿5秒，让页面加载完全
            count += 1
        except urllib.error.HTTPError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        except Exception as e:
            print(e)
    chrome.quit()
    # 对网址进行去重操作
    allUrl = list(set(allUrl))
    return allUrl


'''
作用：爬取某一具体课程的课程名和参加该课程的人数
参数：url是该课程的网址
返回值：该系列课程的课程名和参加该课程的人数
'''


def get_course_data(url):
    # 爬取该课程，获取该课程的网页源代码
    # 因为无法用urllib和request的爬取网页信息，被对方服务器积极拒绝，所以采用模拟浏览器技术
    chrome = webdriver.PhantomJS()
    chrome.get(url)
    data = chrome.page_source
    pat_name = '<span class="course-title f-ib f-vam">(.*?)</span>'
    pat_num = 'enrollCount : "(.*?)"'
    name = re.compile(pat_name).findall(data)  # 返回的是列表
    num = re.compile(pat_num).findall(data)  # 返回的是列表
    if name == [] or num == []:
        return None, None
    else:
        return name[0], num[0]


'''
作用：将课程名和参加课程的人数进行可视化
参数：class_course 是搜索的关键字
    d_name 是课程名
    d_num 是参加该课程的人数
返回值：无
'''


# def show_course_data(class_course, d_name, d_num):
#     bar = Bar(class_course + "系列课程统计图", "x-课程名,y-人数")
#     bar.add("课程", d_name, d_num)
#     bar.show_config()
#     bar.render("D:\\python\\" + class_course + ".html")


def main():
    class_urls = class_course_urls(keywds)
    # 逐个爬取带关键字的课程
    alldata = []  # 用来存放所有系列的课程
    for i in range(0, len(keywds)):
        data = []  # 用来存放某一系列课程的数据
        print('正在爬取带关键字【' + keywds[i] + '】的课程...')
        urls = get_class_course_urls(class_urls[i])
        print('【' + keywds[i] + '】系列课程爬取完毕！')
        print('该系列课程共' + str(len(urls)) + '个！')
        print('这一页爬取的所有课程网址为：', urls)
        # 爬取具体某一课程的数据
        for j in range(0, len(urls)):
            # get_course_data(url)返回的是一个元组，将其添加到data中
            name, num = get_course_data(urls[j])
            # 判断内容是否为空
            if name != None and num != None:
                data.append((name, num))
            print('第' + str(j + 1) + '门课程信息爬取成功！')
        alldata.append(data)
        print(alldata)
        # 对该系列课程做一个可视化
        # 将课程名放在一个列表里
        names = []
        [names.append(x[0]) for x in data]
        # 将参加课程的人数放在一个列表里
        nums = []
        [nums.append(int(x[1])) for x in data]
        print(names)
        print(nums)
        # if names != [] and nums != []:
        #     show_course_data(keywds[i], names, nums)
        # else:
        #     print("数据为空，无法可视化！")


if __name__ == '__main__':
    main()
