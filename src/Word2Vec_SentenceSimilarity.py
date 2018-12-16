
import os
from ToolClasses import IO


def readTopics(groupTopicspath,eventTopicspath):
    groupTopics = IO.csv_reader(groupTopicspath)
    # print(len(groupTopics))
    gtopics = []
    [gtopics.append([i[0], i[2], i[3]]) for i in groupTopics]
    for item in gtopics:
        print(item)

    eventTopics = IO.csv_reader(eventTopicspath)
    # print(len(eventTopics))
    etopics = []
    [etopics.append([i[0], i[1],i[3]]) for i in eventTopics]
    for item in etopics:
        print(item)
    return gtopics,etopics

def computeSimilarityWord2Vec(sentence1,sentence2):



    return 0

def main():
    eventTopicspath = os.getcwd() + "\\..\\Data\\GroupEvents\\Group_45494\\Group_45494_events.csv"
    groupTopicspath = os.getcwd()+"\\..\\Data\\GroupEvents\\Group_45494\\Group_45494_topics.csv"
    gtopics, etopics = readTopics(groupTopicspath, eventTopicspath)
    # for etopic in etopics:
    #     list = []
    #      for gtopic in gtopics:
    #



if __name__ == "__main__":
    main()