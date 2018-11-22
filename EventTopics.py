import os
import csv
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import gensim


################################################################
#①读取events文件，获取event的id和description；
#②数据预处理，数据清洗；
#③利用LDA模型进行主题分析；
#Author：FlashXT;
#Date:2018.11.13,Tuesday;
#CopyRight © 2018-2020,FlashXT & turboMan . All Right Reserved.
################################################################


def readGroupEvents(path=os.getcwd()+"\\Testevents.txt"):
    '''
    读取events文件，获取event的 id,description;
    :param path: 文件路径；
    :return:
    '''
    doc = ""
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            doc = doc + line.strip('\n') # 一行一行的读
        f.close()
    return doc


def main():
    #读取文档
    doc = readGroupEvents()
    print(doc)

    #清洗文档
    tokenizer = RegexpTokenizer(r'\w+')
    raw = doc.lower()
    tokens = tokenizer.tokenize(raw)
    print(tokens)
    # create English stop words list
    en_stop = get_stop_words('en')
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    print(stopped_tokens)
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    # stem token
    texts= [p_stemmer.stem(i) for i in stopped_tokens]
    print(texts)
    dictionary = gensim.corpora.Dictionary([texts])
    print(dictionary.token2id)
    corpus = [dictionary.doc2bow(texts)]
    print(corpus[0])
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)
    print(ldamodel.print_topics(num_topics=3, num_words=1))
if __name__=="__main__":
    main()