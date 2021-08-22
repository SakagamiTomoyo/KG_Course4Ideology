import os
import jieba
import jieba.analyse as analyse
import sklearn
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt

def countIdf(corpus):
    vectorizer = CountVectorizer(analyzer='word')  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    # word=vectorizer.get_feature_names()#获取词袋模型中的所有词
    # for j in range(len(word)):
    #     if weight[1][j]!=0:
    #         print(word[j], weight[1][j])
    return weight


def get_classification(k):
    file_list = []
    with open('stopword.txt', 'r', encoding='utf-8') as reader:
        for line in reader.readlines():
            stop_list.append(line.replace('\n', ''))

    for file in os.listdir(input_dir):
        if '.txt' not in file:
            continue
        file_list.append(file[:-4])
        course_name = file.split('_')[0]
        cut = jieba.lcut(course_name)
        words = ''
        for word in cut:
            if word not in stop_list:
                words = words + word + ' '
        with open(input_dir + '\\' + file, 'r', encoding='utf-8') as reader:
            for line in reader.readlines():
                cut = jieba.lcut(line)
                for word in cut:
                    if word not in stop_list:
                        words = words + word + ' '

        corpus.append(words.strip())
        course_name_list[words.strip()] = course_name
        # corpus.append(' '.join(course_name))

    distortions = []
    for i in range(1, 200):
        mykms = KMeans(n_clusters=i, init='k-means++')
        y = mykms.fit_predict(countIdf(corpus))
        distortions.append(mykms.inertia_)
        print(distortions[-1])
    # for i in range(len(corpus)):
    #     print(corpus[i], y[i])
    plt.plot(range(1, 200), distortions)
    plt.show()

    mykms = KMeans(n_clusters=k, init='k-means++')
    y = mykms.fit_predict(countIdf(corpus))
    for i in range(len(corpus)):
        print(corpus[i], y[i])

    with open(output_dir + '/classification_res.txt', 'w', encoding='utf-8') as w:
        for i in range(k):
            for j in range(len(y)):
                if y[j] == i:
                    w.write(file_list[j] + '\t' + course_name_list[corpus[j]] + '\t' + str(y[j]) + '\n')
        # for j in range(len(y)):
        #     w.write(file_list[j] + '\t' + corpus[j].replace(' ', '') + '\t' + str(y[j]) + '\n')


input_dir = '../data/mooc/computer_channel'
output_dir = '../data/entities'

course_name_list = {}
corpus = []
stop_list = ['（', '）', '(', ')', '—', '上', '中', '下', '的', '\n', '\t']


def longestCommonSequence(str_one, str_two, case_sensitive=True):
    """
    str_one 和 str_two 的最长公共子序列
    :param str_one: 字符串1
    :param str_two: 字符串2（正确结果）
    :param case_sensitive: 比较时是否区分大小写，默认区分大小写
    :return: 最长公共子序列的长度
    """
    len_str1 = len(str_one)
    len_str2 = len(str_two)
    # 定义一个列表来保存最长公共子序列的长度，并初始化
    record = [[0 for i in range(len_str2 + 1)] for j in range(len_str1 + 1)]
    for i in range(len_str1):
        for j in range(len_str2):
            if str_one[i] == str_two[j]:
                record[i + 1][j + 1] = record[i][j] + 1
            elif record[i + 1][j] > record[i][j + 1]:
                record[i + 1][j + 1] = record[i + 1][j]
            else:
                record[i + 1][j + 1] = record[i][j + 1]

    return record[-1][-1]


def get_intersection():
    res = []
    with open(output_dir + '/classification_res.txt', 'r', encoding='utf-8') as reader:
        class_ind = 0
        intersection = ''
        for line in reader.readlines():
            name, id = line.replace('\n', '').split(' ')
            if id != class_ind:
                res.append(intersection)
                intersection = name
            else:
                intersection = longestCommonSequence(intersection, name, case_sensitive=False)


def get_min_length_name(k):
    type_course = {}
    type_entity = {}
    with open(output_dir + '/classification_res.txt', 'r', encoding='utf-8') as reader, \
            open(output_dir + '/course_entity.txt', 'w', encoding='utf-8') as entity_writer, \
            open(output_dir + '/course_entity_concrete.txt', 'w', encoding='utf-8') as course_writer, \
            open(output_dir + '/rel.txt', 'w', encoding='utf-8') as rel_writer:
        for line in reader.readlines():
            course, entity, type = line.replace('\n', '').split('\t')
            if type not in type_course.keys():
                type_course[type] = [course]
            else:
                type_course[type].append(course)
            if type not in type_entity.keys():
                type_entity[type] = entity
            else:
                if len(entity) < len(type_entity[type]):
                    type_entity[type] = entity
        print(type_entity)
        print(type_course)

        course_ind = 0

        for i in range(k):
            for type_1, entity in type_entity.items():
                for type_2, course in type_course.items():
                    if int(type_1) == int(type_2) and int(type_1) == i:
                        entity_writer.write(str(i) + '\t' + entity + '\n')
                        for item in course:
                            course_writer.write(str(course_ind) + '\t' + item + '\n')
                            rel_writer.write(str(i) + '\t' + str(course_ind) + '\n')
                            course_ind += 1


def get_max_weight():
    res = []
    with open(output_dir + '/classification_res.txt', 'r', encoding='utf-8') as reader:
        class_ind = 0
        intersection = ''
        for line in reader.readlines():
            name, id = line.replace('\n', '').split(' ')
            print(analyse.extract_tags(name, topK=3, withWeight=True))
            # if id != class_ind:
            #     res.append(intersection)
            #     intersection = name
            # else:
            #     if len(name) < len(intersection):
            #         intersection = name
            class_ind = id
    res.remove('')
    return res


if __name__ == '__main__':
    k = 80
    # print(longestCommonSequence('Web前端开发', 'Web编程技术'))
    get_classification(k)
    # get_intersection()
    get_min_length_name(k)
    # print(course_entity)
    # get_max_weight()
