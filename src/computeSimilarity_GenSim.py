###########################################################
#计算利用通过eventname 使用LDA算法提取的 event topic 与group
# topics的相似度，并进行匹配；
#
#
#
###########################################################
import nltk
from ToolClasses import IO
from nltk.corpus import wordnet as wn

def computeSimilarity(gtopic,etopic):
    wordlist = nltk.pos_tag([gtopic,etopic])

    print(wordlist[0][0])
    print(wordlist[0][1])
    word1 = wn.synset(wordlist[0][0] )
    print(word1)
    # word2 = wn.synset(etopic+".n.01")

    # gtopicwn = wn.synset(str)
    # etopicwn = wn.synset(str2)
    # print(gtopicwn)
    # print(etopicwn)
    # return  word1.path_similarity(word2)

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
    # eventTopicspath = os.getcwd()+"\\..\\Data\\GroupEvents\\Group_45494\\Model\\group45494Topics.csv"
    # groupTopicspath = os.getcwd()+"\\..\\Data\\GroupEvents\\Group_45494\\Group_45494_topics.csv"
    # gtopics, etopics = readTopics(groupTopicspath, eventTopicspath)
    # print(gtopics)
    # print(nltk.pos_tag(gtopics))
    photography = wn.synset('photography.n.01')
    photoshoot = wn.synset('photoshoot.n.01')
    print(photography.path_similarity(photoshoot))
    # print(computeSimilarity("cat", "dog"))
    return 0

if __name__ == "__main__":
    main()