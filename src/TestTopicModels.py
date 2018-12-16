# -*- coding:utf-8 -*-
import os
from ToolClasses import IO
from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models


if __name__ == "__main__":

    corpus = []   # 存储文档
    tokens = []   # 存储文档中的单词
    # 读取文档的操作

    path = os.getcwd() + "\\Data\\GroupEvents\\Group_45494\\Group_45494_events.csv"
    temp = []
    corpus = IO.csv_reader(path)
    [temp.append([i[0],i[1],i[10]]) for i in corpus]
    corpus = temp
    print(len(corpus))

    # 去标点符号，去截止词的操作
    file = os.getcwd() + "\\Data\\stopwords.txt"
    f = open(file, "r")
    mystopwords = f.read()
    mystopwords = mystopwords.split('\n')
    en_stop = set()
    for word in mystopwords:
        en_stop.add(word)
    # en_stop = get_stop_words('en')   # 利用Pypi的stop_words包，需要去掉stop_words
    #
    # # 提取主干的词语的操作
    # p_stemmer = PorterStemmer()

    # 分词的操作
    tokenizer = RegexpTokenizer(r'[a-z]+')
    for text in corpus:

        raw = text[2].lower()
        token = tokenizer.tokenize(raw)

        stop_remove_token = [word for word in token if word not in en_stop and len(word) > 3]
        # stem_token = [p_stemmer.stem(word) for word in stop_remove_token]
        tokens.append(stop_remove_token)

    #
    # 得到文档-单词矩阵 （直接利用统计词频得到特征）
    dictionary = corpora.Dictionary(tokens)   # 得到单词的ID,统计单词出现的次数以及统计信息
    print(dictionary.token2id)         # 可以得到单词的id信息  <dict>
    print(type(dictionary))            # 得到的是gensim.corpora.dictionary.Dictionary的class类型

    texts = [dictionary.doc2bow(text) for text in tokens]    # 将dictionary转化为一个词袋，得到文档-单词矩阵

    # 直接利用词频作为特征来进行处理
    lda_model = models.ldamodel.LdaModel(texts, num_topics=82, id2word=dictionary,  passes=500)
    print(lda_model.print_topics(num_topics=3,num_words=1))
    corpus_lda = lda_model[texts]
    for doc in corpus_lda:
        print(doc)
    #
    # # 利用tf-idf来做为特征进行处理
    # texts_tf_idf = models.TfidfModel(texts)[texts]     # 文档的tf-idf形式(训练加转换的模式)
    # # # for text in texts_tf_idf:            # 逐行打印得到每篇文档的每个单词的TD-IDF的特征值
    # # #     print text
    # # lda_tf_idf = models.LdaModel(texts_tf_idf, num_topics=3, id2word=dictionary, update_every=0, passes=200)
    # # print lda_tf_idf.print_topics(num_topics=3,num_words=4)
    # # # doc_topic = [a for a in lda_tf_idf[texts_tf_idf]]
    # # # for topic_id in range(3):
    # # #     print "topic:{}".format(topic_id+1)
    # # #     print lda_tf_idf.show_topic(topic_id)
    # # corpus_lda_tfidf = lda_tf_idf[texts_tf_idf]
    # # for doc in corpus_lda_tfidf:
    # #     print doc
    #
    # # 利用lsi做主题分类的情况
    # print "**************LSI*************"
    # lsi = models.lsimodel.LsiModel(corpus=texts, id2word=dictionary, num_topics=3)    # 初始化一个LSI转换
    # texts_lsi = lsi[texts_tf_idf]                # 对其在向量空间进行转换
    # print lsi.print_topics(num_topics=3, num_words=4)
    # for doc in texts_lsi:
    #     print doc
    #
    # # 利用LDA做主题分类的情况
    # print "**************LDA*************"
    # lda = models.ldamodel.LdaModel(corpus=texts, id2word=dictionary, num_topics=3,update_every=0,passes=20)
    # texts_lda = lda[texts_tf_idf]
    # print lda.print_topics(num_topics=3, num_words=4)
    # for doc1 in texts_lda:
    #     print(doc1)