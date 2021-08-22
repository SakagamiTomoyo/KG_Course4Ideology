def add_link():
    with open('data/import2neo4j/courses.txt', 'r', encoding='utf-8') as r, \
            open('data/import2neo4j/courses2.txt', 'w', encoding='utf-8') as w:
        for line in r.readlines():
            lines = line.split('\t')
            w.write(line.replace('\n', '') + '\t' + 'data/courses/' + lines[-1] + '\n')


def is_chinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def integrate_news(path, count):
    with open(path, 'r', encoding='utf-8') as r, open('data\\news.txt', 'a', encoding='utf-8') as w:
        for line in r.readlines():
            lines = line.split('\t')
            if len(lines) == 1:
                break
            title = lines[0]
            url = lines[1]
            if is_chinese(url):
                url = lines[0]
                title = lines[1]
            w.write(str(count) + '\t' + path.split('\\')[-2] + '\t' + url.replace('\n', '') + '\t' + title.replace('\n', '') + '\n')
            count += 1
    return count


def integrate_papers(path, count):
    with open(path, 'r', encoding='utf-8') as r, open('data\\papers.txt', 'a', encoding='utf-8') as w:
        for line in r.readlines():
            w.write(str(count) + '\t' + path.split('\\')[-2] + '\t' + line.replace('\n', '') + '\n')
            count += 1
    return count


def gci(path, func, count):
    import os
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            count = gci(filepath, func, count)
        else:
            if 'list.txt' in file:
                # print(filepath)
                count = func(filepath, count)
                # print(count)
    return count


def news_course():
    with open('data\\news.txt', 'r', encoding='utf-8') as r, \
            open('data\\import2neo4j\\courses.txt', 'r', encoding='utf-8') as course_r, \
            open('data\\import2neo4j\\chapters.txt', 'r', encoding='utf-8') as course_c, \
            open('data\\news_course.txt', 'w', encoding='utf-8') as news_course, \
            open('data\\news_chapter.txt', 'w', encoding='utf-8') as news_chapter, \
            open('data\\news_section.txt', 'w', encoding='utf-8') as news_section:
        course_list = {}
        for line in course_r.readlines():
            course_list[line.split('\t')[1]] = line.split('\t')[0]

        chapter_list = {}
        for line in course_c.readlines():
            chapter_list[line.split('\t')[2]] = line.split('\t')[1]

        print(chapter_list)

        for line in r.readlines():
            lines = line.split('\t')
            if is_chinese(lines[1]):
                for course in course_list.keys():
                    if lines[1] in course:
                        # print(course)
                        news_course.write(lines[0] + '\t' + course_list[course] + '\n')
                for chapter in chapter_list.keys():
                    if lines[1] in chapter:
                        print(chapter)
                        news_chapter.write(lines[0] + '\t' + chapter_list[chapter] + '\n')
            else:
                news_section.write(lines[0] + '\t' + lines[1] + '\n')


def paper_courses():
    with open('data\\papers.txt', 'r', encoding='utf-8') as r, \
            open('data\\import2neo4j\\courses.txt', 'r', encoding='utf-8') as course_r, \
            open('data\\paper_course.txt', 'w', encoding='utf-8') as paper_course:

        course_list = {}
        for line in course_r.readlines():
            course_list[line.split('\t')[1]] = line.split('\t')[0]

        for line in r.readlines():
            lines = line.split('\t')
            for course in course_list.keys():
                if lines[1] in course:
                    paper_course.write(lines[0] + '\t' + course_list[course] + '\n')


if __name__ == '__main__':
    # path = 'data/papers/'
    # func = integrate_papers
    # gci(path, func, 0)
    # news_course()
    paper_courses()
