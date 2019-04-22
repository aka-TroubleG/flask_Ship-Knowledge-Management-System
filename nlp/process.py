import jieba
import jieba.analyse
import os
import sys
# 引入TF-IDF关键词抽取接口
from nlp import loader

tfidf = jieba.analyse.extract_tags

class nlp:
    def __init__(self, filename):
        self.filename = filename
        self.loader = loader.loader(self.filename)
        self.read_file()

    def read_file(self):
        file_suffix = os.path.splitext(self.filename)
        # print(file_suffix[-1])
        if(file_suffix[-1] == '.txt'):
            self.text = self.loader.read_txt()
        elif(file_suffix[-1] == '.pdf'):
            self.text = self.loader.read_pdf()
        elif(file_suffix[-1] == '.docx'):
            self.text = self.loader.read_word()
        else:
            print('读取文件失败！')
            sys.exit()
        # print(self.text)

    # 基于TF-IDF算法进行关键词抽取
    def keyword_extraction(self):
        keywords = tfidf(self.text , withWeight=True)
        # print("基于TF-IDF算法:")
        # print("提取关键字:")
        # 输出抽取出的关键词
        # for keyword in keywords:
        #     print(keyword + "/", )
        # for i in range(5):
        #     print(keywords[i]+ "/")
        print("提取关键字成功")
        return keywords

    #分词
    def cut(self):
        seg = jieba.cut(self.text,cut_all=True)
        # print("分词结果：")
        # print("/".join(seg))
        return seg

    # def manage(self,path):
    # rootdir = '..\\files'
    # list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    # for i in range(0, len(list)):
    #     path = os.path.join(rootdir, list[i])
    #     if os.path.isfile(path):
            # print("打开"+path+"文件：")
            # test = nlp(path)
            # test.keyword_extraction()
            # test.cut()