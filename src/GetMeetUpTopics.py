#获取New York 州的500个组的信息；
#API: https://api.meetup.com/find/groups
#

import os
import csv
from urllib.parse import *

import requests
import json
from src.config import *


def getTopics(page):

    data={

        'page':page,
        'key': KEY,
        'sign': SIGN,
    }
    group = []
    count = 0
    print("Page : ",end="")
    for offset in range(50):
        url = "https://api.meetup.com/find/topics?"+'offset='+str(offset)+'&'+urlencode(data)
        # print(url)
        response = requests.get(url)

        if response.status_code == 200:

            result = json.loads(response.text)
            for i in range(len(result)):
                # count +=1
                # print( count,'\n ',result[i]["id"], result[i]["status"], result[i]["visibility"])
                if result[i]["status"] == "active" and result[i]["visibility"] == "public"\
                        and result[i]["state"] == "NY":
                    group.append([result[i]["id"],result[i]["name"],result[i]["link"],result[i]["created"],
                                  result[i]["city"],result[i]["state"], result[i]["country"],result[i]["lat"],
                                  result[i]["lon"],result[i]["members"],result[i]["category"]["id"],
                                  result[i]["category"]["name"],result[i]["description"]
                                 ])
            print(str(offset+1),end=" ")
        else:
            print(response.status_code)
    # print()
    # print(len(group))
    return group


def savegroups(state,group):
    path = os.getcwd() + "\\Groups"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "\\GroupsNY50miles.csv", 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["group_id", "group_name", "link", "created", "city","state", "country", "lat",
                         "lon", "members","categoryid","categoryname","description"])
        writer.writerows(group)
        file.close()

    print("\nThe Groups in "+str(state)+" save success!")

def main():
    group = getTopics('US','NY','40.32','-74','50',20)
    savegroups('NYC',group)

if __name__ == "__main__":
    main()