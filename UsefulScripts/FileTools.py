# coding=utf-8
import os


# https://blog.csdn.net/chengxuyuanyonghu/article/details/59486631 学习网址
class FileTools(object):
    def __init__(self):
        pass

    def printAllFileNames(self, inputPath):
        inputPath = str(inputPath)
        for root, dirs, files in os.walk(inputPath):
            for name in files:
                print(os.path.join(root, name))  # todo 写进文本文件中，对输入路径做校验


if __name__ == "__main__":
    FileTools().printAllFileNames(inputPath="C:\CRroot\desktop\SpringiA4_SourceCode")
