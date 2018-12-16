import os
import csv


#CSV文档读取模块
def csv_reader(path):
    try:
        with open(path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            result = []
            for row in reader:
                result.append(row)
            file.close()
        return result
    except Exception as e:
        print(e)

def csv_writer(path,content):

    try:
        with open(path, 'w+', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            # writer.writerow(['groupid','eventid','description'])
            writer.writerows(content)
    except Exception as e:
        print(e)

def readFile(file):
    if not os.path.exists(file):
        return 0
    else :
        f = open(file,"r")
        fileNo = f.readline()
        f.close()
        return fileNo

def writeFile(file,content):

    f = open(file,"w+")
    f.writelines(content)
    f.close()
    return 1