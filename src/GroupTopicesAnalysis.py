
from ToolClasses.IO import *
import matplotlib.pyplot as plt

def topicsSumByGroup(topics):
    topicsum = []
    topicsSummary = []
    i = 0
    temp = 0
    groupid = topics[0][0]
    gtoipcs = [groupid]
    while i < len(topics):
        if topics[i][0] == groupid:
            gtoipcs.append(topics[i][3])
            i = i+1
        else:
            topicsSummary.append(gtoipcs)
            topicsum.append([groupid,i - temp])
            groupid = topics[i][0]
            temp = i
            gtoipcs = []
            gtoipcs.append(topics[i][0])

    return topicsum,topicsSummary


def plotHist(topicsum):
    x = []
    y = []
    for item in topicsum:
        x.append(item[0])
        y.append(item[1])
    # 添加图形属性
    plt.xlabel('Groups')
    plt.ylabel('TopicsNum')
    plt.title('The num of Group Topics')
    # a = plt.subplot(1, 1, 1)
    # plt.ylim=(10, 40000)
    print(x)
    print(y)
    a = x[0:200]
    b = y[0:200]
    plt.bar(x, y, facecolor='blue', width=0.8)
    plt.show()


def main():
    path = os.getcwd()+"\\..\\Data\\GroupTopics\\Grouptopics.csv"
    topics = csv_reader(path)
    # print(len(topics))
    topicsum,topicsSummary = topicsSumByGroup(topics)
    plotHist(topicsum)
    sum  = 0
    for item in topicsum:
        sum  = sum + item[1]
    count = sum // len(topicsum)
    print(count)
    # print(topicsSummary)
    # print(topicsum)


if __name__ == "__main__":
    main()