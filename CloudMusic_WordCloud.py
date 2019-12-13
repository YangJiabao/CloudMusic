import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import csv
import pandas as pd
import os
from collections import defaultdict
import imageio



class CloudMusic:
    def read_stopword(self,fpath):
        """
        读取中文停用词表
        """
        with open(fpath, 'r', encoding='utf-8') as file:
            self.stopword = file.readlines()
        return [word.replace('\n', '') for word in self.stopword]

    def cut_word(self,ser, stop_word):
        """
        使用jieba.cut()对内容提要分词处理,
        :params ser: pd.Series object
        :params stop_word: list or tuple object
        """
        # 删除分词结果中的停用词
        result = [word for word in jieba.cut(ser['评论内容']) if word not in stop_word]
        # 去除分词后长度小于2的词语
        return ' '.join([word for word in result if len(word)>1])


    def count_words(self,word_lists, n):
        """
        计数器函数
        统计词频，并过滤掉词频小于某个阈值 n 的词语
        : params word_lists 二维列表
        """
        frequency = defaultdict(int)  # 实例化对象
        for word_list in word_lists:
            for word in word_list:
                frequency[word] += 1

        # 去除词频小于某一阈值的词语，.items()遍历字典的key以及value
        new_dict = {key: value for key, value in frequency.items() if value > n}
        return new_dict


    def __init__(self):
        jieba.load_userdict("E:/1.txt")#加入不分割的词
        self.fpath = 'E:/wangyiyun/评论/xiaoai2.csv'
        data = pd.read_csv(self.fpath, sep=',', encoding='utf-8-sig', usecols=[0, ])
        data.head()
        # print(data)
        # 加载多个停用词表
        self.path1 = 'E:/'
        name_list = ['stopwords.txt', '哈工大停用词表.txt', '呆萌的停用词表.txt']

        stop_word = []
        for fname in name_list:
            stop_word += self.read_stopword(os.path.join(self.path1, fname))
        stop_word = set(stop_word)  # 停用词表去重

        data['评论内容'] = data.apply(lambda x: pd.Series(self.cut_word(x, stop_word)), axis=1)
        #print(data)

        #将分词结果转化为一个二维列表----------计数器调用
        word_lists = [item.split() for item in data['评论内容']]
        #调用计数器并传入参数，去除词频小于20的词语
        frequency = self.count_words(word_lists, 20)
        #以字典的值对字典排序
        frequency = sorted(frequency.items(), key=lambda d:d[1], reverse=True)
        print(frequency)

        #对象实例化      ------ 制作词云图
        bg_image = np.array(Image.open('E:\wangyiyun\hhhh.jpg'))
        #bg_image = imageio.imread('E:\wangyiyun\hhhh.jpg')
        wc = WordCloud(font_path='C:\Windows\Fonts\STXINGKA.TTF',# 设置显示中文的字体
                       mask=bg_image,  # 设置背景图
                       background_color= 'white',
                       scale=2,  # 原图的几倍
                       colormap='PiYG'
                       )

        content = ' '.join(data['评论内容'].tolist())  # 将所有的分词结果拼接为一个字符串，间隔为一个空格
        #print(content)
        #wc.generate(content)     # 接收字符串文本，生成词云图
        wc.generate(content)#绘制图片


        #保存词云图
        wc.to_file('E:/好想爱这个世界啊词云图.png')
        print('完成!')
        #以下代码为实时展示制作的词云图
        #plt.imshow(wc)
        #plt.axis('off')
        #plt.show()

if __name__ == '__main__':
    WANG = CloudMusic()
