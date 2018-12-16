##################################################################
#LDA算法:
#将所有文档作为语料库，从所有的文档中提取除指定个数的主题；
#
#Author：FlashXT;
#Date:2018.12.9,Sunday;
#CopyRight © 2018-2020,FlashXT & turboMan . All Right Reserved.
###################################################################
import os
import re
import nltk

from ToolClasses import IO
from smart_open import smart_open
from gensim.corpora import Dictionary
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
# from stop_words import get_stop_words
from nltk.corpus import stopwords
from gensim import corpora, models
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

class MyCorpus(object):
    def __iter__(self,path):
        for line in smart_open(path, 'rb'):
            # assume there's one document per line, tokens separated by whitespace
            yield Dictionary.doc2bow(line.lower().split())

class textPreprocess():
    def __init__(self,SourPath,DestPath):
        '''
        预处理类的初始化
        :param SourPath:
        :param DestPath:
        '''
        self.SourPath = SourPath
        self.DestPath = DestPath
        self.content = IO.csv_reader(SourPath)
        list = []
        for item in self.content:
            list.append([item[0],item[1],item[3]])
        self.content = list


    def Preprocessing(self,Modelpath):

        # ①去除HTML标签

        list = []
        for item in self.content:
            content = re.sub(r'<[^>]*>',' ',item[2])
            list.append([item[0],item[1],content])
        self.content = list
        # ②去除除了26个字母,数字以外的字符
        list=[]
        tokenizer = RegexpTokenizer(r'[a-z]+')
        # tokenizer = RegexpTokenizer(r'\w+')
        for item in self.content:
            raw = str(item[2]).lower()
            tokens = tokenizer.tokenize(raw)
            # tokens =" ".join(i for i in tokens)
            list.append([item[0],item[1],tokens])
        self.content = list

        # ③去除停用词
        list = []
        #获取英语的停用词表
        en_stop = set(stopwords.words('english'))     # get_stop_words('en')
        file = os.getcwd()+"\\..\\Data\\stopwords.txt"
        f = open(file, "r")
        mystopwords = f.read()
        mystopwords= mystopwords.split('\n')
        # print(len(en_stop))
        for word in mystopwords:
            en_stop.add(word)
        # print(len(en_stop))
        #去除文本中的停用词

        for item in self.content:

            stopped_tokens = [i for i in item[2] if not i in en_stop]
            stopped_tokens = " ".join(i for i in stopped_tokens)

            list.append([item[0],item[1],stopped_tokens])

        # ④ 按词性和长度过滤
        wordtag = []
        for item in list:

            content = nltk.pos_tag(item[2].split(" "))

            temp=[i[0] for i in content if i[1]=="NN" and len(i[0])>3]

            wordtag.append(temp)

        for item in wordtag:
            print(item)
        self.content = wordtag

        # ⑤ 生成字典和语料库
        # 分词器:将句子(list类型)切分为单词
        p_stemmer = PorterStemmer()
        texts = [p_stemmer.stem(" ".join(i)) for i in wordtag]

        # corpora.Dictionary 对象
        # 类似python中的字典对象, 其Key是字典中的词，其Val是词对应的唯一数值型ID
        dictionary = corpora.Dictionary(text.split() for text in texts)
        # print(dictionary.token2id)
        # dictionary.doc2bow(doc)是把文档 doc变成一个稀疏向量，[(0, 1), (1, 1)]，
        # 表明id为0,1的词汇出现了1次。 \
        corpus = [dictionary.doc2bow(text.split()) for text in texts]


        # 存储字典和语料库
        if not os.path.exists(Modelpath):
            os.mkdir(Modelpath)
        dictionary.save(os.path.join(Modelpath, 'group45494.dict'))  # store the dictionary, for future reference
        corpora.MmCorpus.serialize(os.path.join(Modelpath, 'group45494.mm'), corpus)

        return corpus,dictionary

    def LDAModeling(self,Modelpath):
        '''

        :return:
        '''

        if os.path.exists(os.path.join(Modelpath, 'group45494.dict')):

            # 加载字典和语料库
            dictionary = corpora.Dictionary.load(os.path.join(Modelpath, 'group45494.dict'))
            corpus = corpora.MmCorpus(os.path.join(Modelpath, 'group45494.mm'))
        else :
            corpus, dictionary = self.Preprocessing(Modelpath)
        ldamodel = models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=200)
        for item in ldamodel.print_topics(num_topics=10, num_words=1):
            print(item)

        # for item in  ldamodel.print_topics(num_topics=3, num_words=1):
        #     list.append([self.content[1][0],item])
        # path = os.getcwd()+"\\Data\\Group_12542_eventsTopics.csv"
        # IO.csv_writer(path, list)


def main():

    Sourpath = os.getcwd()+"\\..\\Data\\GroupEvents\\Group_45494\\Group_45494_events.csv"
    corpuspath = os.getcwd()+"\\..\\Data\\GroupEvents\\Group_45494\\Group_45494_eventsProcessed.csv"
    ModelPath = os.getcwd()+"\\..\\Data\\GroupEvents\\Group_45494\\Model"
    text = textPreprocess(Sourpath,corpuspath)
    # text.Preprocessing(ModelPath)
    text.LDAModeling(ModelPath)

if __name__ == "__main__":
    main()
