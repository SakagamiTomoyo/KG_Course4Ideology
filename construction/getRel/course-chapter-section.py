import os
import jieba.analyse as analyse
import jieba.posseg as posseg

import re

def choose():
    dict_university_course = {}

    for file in os.listdir('../data/mooc/computer_channel'):
        if file == '新建文件夹':
            continue
        name = file.split('_')[0].replace('（上）', '').replace('（下）', '').replace('（中）', '')
        university = file.split('_')[1]
        key = analyse.extract_tags(name.lower(), topK=3, withWeight=True)
        print(name, key)

        if university not in dict_university_course.keys():
            dict_university_course[university] = [name]
        else:
            dict_university_course[university].append(name)

    for k, v in dict_university_course.items():
        print(k, v)


def find_keyword(content, reader, index):
    # if ' ' in content:
    #     content = content.split(' ')[-1]
    # list_keyword = analyse.extract_tags(content, topK=10)

    list_keyword_and_tokenize = posseg.lcut(content)
    list_keyword = []

    print(list_keyword_and_tokenize)
    for word in list_keyword_and_tokenize:
        # if word.word.isdigit() or '.' in word:
        #     list_keyword_and_tokenize.remove(word)
        if 'n' in word.flag or 'eng' in word.flag:
            list_keyword.append(word.word)
    print(list_keyword)
    reader.write(str(index) + '\t' + '\t'.join(list_keyword) + '\n')


def course_entity():
    course_id = 0
    chapter_id = -1
    section_id = 0
    start_tag = ['课程大纲']
    end_tag = ['证书要求', '常见问题', '预备知识', '参考资料']
    drop = ['测验', '导学', '讨论', '总结', '循序渐进', '小结', '作业']



    with open('../data/entities/courses.txt', 'w', encoding='utf-8') as course_writer, \
        open('../data/entities/chapters.txt', 'w', encoding='utf-8') as chapter_writer, \
        open('../data/entities/sections.txt', 'w', encoding='utf-8') as section_writer, \
        open('../data/entities/chapter_keywords.txt', 'w', encoding='utf-8') as chapter_keyword_writer, \
        open('../data/entities/section_keywords.txt', 'w', encoding='utf-8') as section_keyword_writer:
        for file in os.listdir(path):
            if '.txt' not in file:
                continue
            name = file.split('_')[0].replace('.txt', '').replace('\t', ' ')
            if '-' in name:
                name = name.split('-')[1]
            if ' ' in name:
                name = name.split(' ')[0]
            course_writer.write(str(course_id) + '\t' + name + '\t' + file.replace('.txt', '') + '\n')

            with open(path + '/' + file, 'r', encoding='utf-8') as reader:
                contents = []
                status = 0
                pre_header = ''
                for line in reader.readlines():
                    if status == 0:
                        if line.replace('\n', '') in start_tag:
                            status = 1
                    elif status == 1:
                        content = line.replace('\n', '').replace('\t', ' ').replace(' ', '').lower()
                        if content in end_tag:
                            status = 2
                        else:
                            if len(content) > 0 and content not in contents:

                                # continue_tag = False
                                # for word in drop:
                                #     if word in content:
                                #         continue_tag = True
                                #
                                # if continue_tag:
                                #     print(content)
                                #     continue

                                contents.append(content)
                                if '第' in content and '讲' in content:
                                    header = content[content.index('第'): content.index('讲') + 1]
                                    print(header)
                                    if header != pre_header:
                                        pre_header = header
                                        chapter_id += 1
                                        chapter_writer.write(str(course_id) +
                                                             '\t' + str(chapter_id) + '\t' + content + '\n')
                                        find_keyword(content, chapter_keyword_writer, chapter_id)

                                elif '第' in content and '章' in content:
                                    header = content[content.index('第'): content.index('章') + 1]
                                    print(header)
                                    if header != pre_header:
                                        pre_header = header
                                        chapter_id += 1
                                        chapter_writer.write(str(course_id) +
                                                             '\t' + str(chapter_id) + '\t' + content + '\n')
                                        find_keyword(content, chapter_keyword_writer, chapter_id)

                                elif '第' in content and '周' in content:
                                    header = content[content.index('第'): content.index('周') + 1]
                                    print(header)
                                    if header != pre_header:
                                        pre_header = header
                                        chapter_id += 1
                                        chapter_writer.write(str(course_id) +
                                                             '\t' + str(chapter_id) + '\t' + content + '\n')
                                        find_keyword(content, chapter_keyword_writer, chapter_id)

                                elif '第' in content and '单元' in content:
                                    header = content[content.index('第'): content.index('单元') + 2]
                                    print(header)
                                    if header != pre_header:
                                        pre_header = header
                                        chapter_id += 1
                                        chapter_writer.write(str(course_id) +
                                                             '\t' + str(chapter_id) + '\t' + content + '\n')
                                        find_keyword(content, chapter_keyword_writer, chapter_id)

                                elif '第' in content and '篇' in content:
                                    header = content[content.index('第'): content.index('篇') + 1]
                                    print(header)
                                    if header != pre_header:
                                        pre_header = header
                                        chapter_id += 1
                                        chapter_writer.write(str(course_id) +
                                                             '\t' + str(chapter_id) + '\t' + content + '\n')
                                        find_keyword(content, chapter_keyword_writer, chapter_id)

                                elif content.isdigit():
                                    header = content
                                    print(header)
                                    if header != pre_header:
                                        pre_header = header
                                        chapter_id += 1
                                        chapter_writer.write(str(course_id) +
                                                             '\t' + str(chapter_id) + '\t' + content + '\n')

                                    chapter_keyword_writer.write(str(chapter_id) + '\n')


                                else:
                                    section_writer.write(str(chapter_id) + '\t' + str(section_id) + '\t' + content + '\n')
                                    section_id += 1
                                    find_keyword(content, section_keyword_writer, section_id)
                    else:
                        continue
            course_id += 1


if __name__ == '__main__':
    # print('01'.isdigit())
    path = '../data/mooc/computer_channel/filter'
    course_entity()

    # print(re.findall('第\d*(章|周|单元)', '第111单元'))
