###########################################################
#计算利用通过eventname 使用LDA算法提取的 event topic 与group
# topics的相似度，并进行匹配；
#
#
#
###########################################################
import os
from ToolClasses import IO
from nltk.corpus import wordnet as wn

def computeSimilarity(gtopic,etopic):

    gtopicwn = wn.synset(gtopic).defnition()
    etopicwn = wn.synsets(etopic).defnition()
    return  gtopicwn.path_similartity(etopicwn)

def readTopics(groupTopicspath,eventTopicspath):
    groupTopics = IO.csv_reader(groupTopicspath)
    # print(len(groupTopics))
    gtopics = []
    [gtopics.append([i[0], i[2], i[3]]) for i in groupTopics]
    # for item in gtopics:
    #     print(item)

    eventTopics = IO.csv_reader(eventTopicspath)
    # print(len(eventTopics))
    etopics = []
    [etopics.append([i[0], i[1]]) for i in eventTopics]
    # for item in etopics:
    #     print(item)
    return gtopics,etopics

def main():
    eventTopicspath = os.getcwd()+"\\..\\Data\\GroupEvents\\Group_45494\\Model\\group45494Topics.csv"
    groupTopicspath = os.getcwd()+"\\..\\Data\\GroupEvents\\Group_45494\\Group_45494_topics.csv"
    gtopics, etopics = readTopics(groupTopicspath, eventTopicspath)
    computeSimilarity("cat", "dog")
    return 0

if __name__ == "__main__":
    main()