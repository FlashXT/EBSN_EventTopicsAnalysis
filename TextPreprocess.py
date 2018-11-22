################################################################
#文本预处理:对Event的描述字段进行处理;
#①去除HTML标签；
#②起初非文本信息；
#
#Author：FlashXT;
#Date:2018.11.21,Wednesday;
#CopyRight © 2018-2020,FlashXT & turboMan . All Right Reserved.
################################################################
import re
from IO import *
import gensim
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer


class textPreprocess():
    def __init__(self,SourPath,DestPath):
        '''
        预处理类的初始化
        :param SourPath:
        :param DestPath:
        '''
        self.SourPath = SourPath
        self.DestPath = DestPath
        self.content = csv_reader(SourPath)
        list = []
        for item in self.content:
            list.append([item[0],item[10]])
        self.content = list


    def Preprocess1(self,destpath1):
        '''
        去除HTML标签
        :return:
        '''
        list = []
        for item in self.content:
            content = re.sub(r'<[^>]*>',' ',item[1])
            list.append([item[0],content])

        csv_writer(destpath1,list)
        self.content = list


    def Preprocess2(self,destpath2):
        '''
        去除除了26个字母,数字以外的字符
        :return:
        '''
        list = []
        tokenizer = RegexpTokenizer(r'[a-z0-9]+')
        # tokenizer = RegexpTokenizer(r'\w+')
        for item in self.content:
            raw = str(item[1]).lower()
            tokens = tokenizer.tokenize(raw)
            list.append([item[0],tokens])

        csv_writer(destpath2,list)
        self.content = list


    def Preprocess3(self,destpath3):
        '''
        去除停用词
        :return: 
        '''
        #获取英语的停用词表
        en_stop = get_stop_words('en')
        #去除文本中的停用词
        list = []
        for item in self.content:
            stopped_tokens = [i for i in item[1] if not i in en_stop]
            list.append([item[0],stopped_tokens])

        csv_writer(destpath3,list)
        self.content = list


        
        
def main():
    Sourpath = os.getcwd()+"\\Data\\Group_12542_events.csv"
    Destpath = os.getcwd()+"\\Data\\Group_12542_eventsPreProcessed.csv"
    destpath1 = os.getcwd() + "\\Data\\Group_12542_eventsPreProcessed1.csv"
    destpath2 = os.getcwd() + "\\Data\\Group_12542_eventsPreProcessed2.csv"
    # destpath3 = os.getcwd() + "\\Data\\Group_12542_eventsPreProcessed3.csv"
    text = textPreprocess(Sourpath,Destpath)
    text.Preprocess1(Destpath)
    text.Preprocess2(destpath1)
    text.Preprocess3(destpath2)

if __name__ == "__main__":
    main()
