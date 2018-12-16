####################################################################
#Class PlotTopics(): 该函数用来绘制事件topics的条形统计图；
#   function: EventTopicCount(path)用来统计不同topic的数量；
#         path 为要绘制的文件路径；该文件的格式如下：
#                   ========================
#                   eventorder,eventTopic
#                   0,street
#                   1,bridal
#                   2,cruise
#                   3,body
#                   4,party
#                   5,cruise
#                   =========================
#   function plotHist():根据EventTopicsCount函数的统计结果进行绘图；
#Author：FlashXT;
#Date:2018.12.16,Sunday;
#CopyRight © 2018-2020,FlashXT & turboMan . All Right Reserved.
#####################################################################

import os
from ToolClasses import IO
import matplotlib.pyplot as plt

class PlotTopics():
    def __init__(self,path):

        topicdic = EventTopicCount(path)
        plotHist(topicdic)

def EventTopicCount(path):

    # list  = []
    # if os.path.isdir:
    #     list = os.listdir(path)
    #
    # for item in list:
    #     if item.split(".")[1] == "csv":
    #eventTopic =  IO.csv_reader(os.path.join(path,item))
    eventTopic =  IO.csv_reader(path)

    topic = []
    [topic.append(i[1]) for i in eventTopic]
    i = 0
    topicdic = {}
    while i < len(topic):

        if topic[i] in topicdic.keys():
            topicdic[str(topic[i])] = topicdic[str(topic[i])] +1
        else:
            topicdic[str(topic[i])] = 1
        i = i + 1
    # for key,value in topicdic.items():
    #     print(key,":",value)
    return topicdic

def plotHist(topicdic):
    x = []
    y = []
    for key,value in topicdic.items():
        if value > 2:
            x.append(key)
            y.append(value)

    # 添加图形属性
    fig = plt.figure(figsize=(10.0, 10.0))
    ax = plt.subplot()
    ax.bar(x, y, facecolor='green', width=0.8)

    plt.xlabel('Topics')
    plt.ylabel('TopicsCount')
    plt.title('The Statistics of Group45494 Events Topics')

    # plt.bar(x, y, facecolor='green', width=0.8)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
    plt.show()

    return 0



# def main():
#     # path = os.getcwd() + "\\..\\Data\\GroupEvents\\Group_45494\\group45494EventsTopics.csv"
#     # print(path)
#     path = os.getcwd() + "\\..\\Model\\eventTopics.csv"
#     # print(path)
#     topicdic = EventTopicCount(path)
#     plotHist(topicdic)

# if __name__ == "__main__":
#     main()