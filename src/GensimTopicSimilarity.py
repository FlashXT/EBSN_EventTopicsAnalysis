###################################################################
#
#将所有事件的name,description作为语料库(每个事件一行)，从所有的事件中提取除
#指定个数的主题(主题维度)；将主题维度与Group Topics 进行映射;
#Author：FlashXT;
#Date:2018.12.14,Friday;
#CopyRight © 2018-2020,FlashXT & turboMan . All Right Reserved.
###################################################################
import os
import re

import nltk

from ToolClasses import IO
from nltk import RegexpTokenizer
from smart_open import smart_open
from gensim.corpora import Dictionary
from nltk.corpus import stopwords
from gensim import corpora, models

# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import warnings

from ToolClasses.PlotEventTopics import PlotTopics

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

class MyCorpus(object):
    def __iter__(self,path):
        for line in smart_open(path, 'rb'):
            # assume there's one document per line, tokens separated by whitespace
            yield Dictionary.doc2bow(line.lower().split())

class textPreprocess():
    def __init__(self,Sourpath):
        '''
        预处理类的初始化
        :param Sourpath:
        '''
        self.SourPath = Sourpath
        self.content = IO.csv_reader(Sourpath)
        list = []
        for item in self.content:
            list.append([item[3],item[10]])
        self.content = list

    def processText(self,Estr):
        # ① 去除HTML标签
        content = re.sub(r'<[^>]*>', ' ', Estr)

        # ② 除去标点符号,等非字母的字符
        tokenizer = RegexpTokenizer(r'[a-z]+')
        raw = str(content).lower()
        content = tokenizer.tokenize(raw)

        # ③ 去除停用词
        # 获取英语的停用词表
        en_stop = stopwords.words('english')  # get_stop_words('en')
        # 获取自己的停用词表
        # file = os.getcwd()+"\\..\\datasets\\stopwords.txt"
        # f = open(file, "r")
        # mystopwords = f.read()
        # mystopwords= mystopwords.split('\n')
        # for word in mystopwords:
        #     en_stop.add(word)
        # 去除文本中的停用词
        stopped_tokens = [i for i in content if not i in en_stop]

        # ④ 按长度过滤
        content = [i for i in stopped_tokens if len(i) > 2]

        return content


    def Preprocessing(self,Modelpath):

        # ① 去除HTML标签

        list = []
        for item in self.content:

            content = re.sub(r'<[^>]*>', ' ',item[1])
            list.append((item[0]+" "+content).lower())
        self.content = list
        # ② 除去标点符号,等非字母的字符
        list = []
        tokenizer = RegexpTokenizer(r'[a-z]+')

        for item in self.content:
            raw = str(item).lower()
            tokens = tokenizer.tokenize(raw)
            # tokens =" ".join(i for i in tokens)
            list.append(tokens)
        self.content = list


        # ③ 去除停用词
        list = []
        #获取英语的停用词表
        en_stop = set(stopwords.words('english'))    # get_stop_words('en')

        #获取自己的停用词表
        file = os.getcwd()+"\\..\\Data\\stopwords.txt"
        f = open(file, "r")
        mystopwords = f.read()
        mystopwords= mystopwords.split('\n')
        for word in mystopwords:
            en_stop.add(word)

        #去除文本中的停用词
        for item in self.content:
            stopped_tokens = [i for i in item if not i in en_stop]
            # stopped_tokens = " ".join(i for i in stopped_tokens)
            list.append(stopped_tokens)
        self.content = list

        # ④ 按长度过滤
        list = []
        for item in self.content:
            temp=[i for i in item if len(i)>2]
            list.append(temp)
        self.content = list
        # ⑤ 按词性过滤
        wordtag = []
        for item in list:
            content = nltk.pos_tag(item)
            temp=[i[0] for i in content if i[1]=="NN"]
            wordtag.append(temp)

        self.content = wordtag

        # ⑥ 去掉低词频的词
        all_stems = sum(self.content, [])
        stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
        texts = [[stem for stem in text if stem not in stems_once] for text in self.content]
        self.content = texts
        #
        # ⑦ 生成字典和语料库
        # # 分词器:将句子(list类型)切分为单词
        # p_stemmer = PorterStemmer()
        # texts = [p_stemmer.stem(" ".join(i)) for i in self.content]
        #
        # # corpora.Dictionary 对象,类似python中的字典对象, 其Key是字典中的词，其Val是词对应的唯一数值型ID
        dictionary = corpora.Dictionary(text for text in texts)
        # # print(dictionary.token2id)#输出word与id的对应关系
        # # dictionary.doc2bow(doc)是把文档 doc变成一个稀疏向量，[(0, 1), (1, 1)]，#表明id为0,1的词汇出现了1次。
        corpus = [dictionary.doc2bow(text) for text in texts]
        #
        # 存储字典和语料库
        if not os.path.exists(Modelpath):
            os.mkdir(Modelpath)
        dictionary.save(os.path.join(Modelpath, 'coursera_corpus.dict'))  # store the dictionary, for future reference
        corpora.MmCorpus.serialize(os.path.join(Modelpath, 'coursera_corpus.mm'), corpus)

        return corpus,dictionary

    def Modeling(self,Modelpath):
        '''
        :return:
        '''

        if os.path.exists(os.path.join(Modelpath, 'coursera_corpus.dict')):

            # 加载字典和语料库
            dictionary = corpora.Dictionary.load(os.path.join(Modelpath, 'coursera_corpus.dict'))
            corpus = corpora.MmCorpus(os.path.join(Modelpath, 'coursera_corpus.mm'))

        else :
            corpus, dictionary = self.Preprocessing(Modelpath)
        # print(corpus[0])
        # print(dictionary)
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        modellsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
        print("========================================================")
        print("The Docs Topic Dims:")
        for item in modellsi.print_topics(num_topics=10, num_words=1):
            print("\t\t",item)
        print("========================================================")
        list =[]
        count = 0
        for item in corpus:
            modellsi = models.LsiModel([item], id2word=dictionary, num_topics=1)
            item = modellsi.print_topics(num_topics=1, num_words=1)
            list.insert(count,[count,item[0][1].split("*")[1].strip('"')])
            count = count +1

        list.insert(0, ["eventorder", "eventTopic"])
        IO.csv_writer(os.path.join(Modelpath, 'eventTopics.csv'), list)

        # index = similarities.MatrixSimilarity(penthouse)
        # print(index)
        # ml_event = self.content[3]
        # print(ml_event[0])
        # ml_bow = dictionary.doc2bow(self.processText(ml_event[1]))
        # ml_lsi = modellsi[ml_bow]
        #
        # sims = index[ml_lsi]

        # sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # # print(sort_sims[0:10])
        # print("========================================================")
        # for item in sort_sims[0:10]:
        #     print(item[0],'\t\t',course_name[item[0]],'\t\t',item[1])
        # print("========================================================")
        # modellda = models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=2000)
        # for item in modellda.print_topics(num_topics=10, num_words=1):
        #     print(item)



def main():

    Sourpath = os.getcwd() + "\\..\\Data\\GroupEvents\\Group_45494\\Group_45494_events.csv"

    ModelPath = os.getcwd()+"\\..\\Model"
    plotpath = os.getcwd() + "\\..\\Model\\eventTopics.csv"
    #
    # corpusfile = open(Sourpath,encoding="utf-8")
    # courses = [line.strip() for line in corpusfile]
    # courses_name = [course.split('\t')[0] for course in courses]
    # courses_info = [course.split('\t')[1] for course in courses]
    # courses_content = [course.split('\t')[2] for course in courses]

    # print(courses_name[0])
    # print(courses_info[0])
    # print(courses_content[0])

    # texts_lower = [[word for word in document.lower().split()] for document in courses]
    # print(texts_lower[0])
    #
    # texts_tokenized = [[word.lower() for word in word_tokenize(document.decode('utf-8'))] for document in courses]
    # print(texts_tokenized[0])

    text = textPreprocess(Sourpath)
    text.Modeling(ModelPath)
    plot = PlotTopics(plotpath)




if __name__ == "__main__":
    main()
