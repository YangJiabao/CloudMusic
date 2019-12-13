import json
from Crypto.Cipher import AES  #新的加密模块只接受bytes数据，否者报错，密匙明文什么的要先转码
import base64
import binascii
import random
import requests
import os
import time
import csv

class Music:
    def __init__(self):
        self.url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_1407358755?csrf_token='
        self.proxies= {
                    'http:':'http://121.232.146.184',
                    'https:':'https://144.255.48.197'
                }
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'content-length':'484',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie':'_iuqxldmzr_=32; _ntes_nnid=390bbb3a442ce08c6cd01111e910757f,1575877884788; _ntes_nuid=390bbb3a442ce08c6cd01111e910757f; WM_TID=OuDyyCl2Lg9BVVFBBEMs%2BajT3TEkVK2d; WM_NI=difndpJL1cgfRMt4THN4UQfqSdYePTMqdgPSXA7LP8W%2FVStuJFQ73x%2FQbHNkaN%2BfHEswdaO79d9ScsjOdXH1nT1kdoubhyFFtzP9el%2B44c3b7vpR00CfzjGoA%2BZ%2FgLhYQ0U%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed1d46b98b385a7bb60928a8ba7d54e978b9e84bb3da7b7b696e55b8fe7a8d1ce2af0fea7c3b92aa8b7aa8fe77c8a94ff84e66e9293bcd5d7448eec9bb2e57b91bc9786d3608fafac88d3599c9ff9add33495f19ab4f77f8a9a9fd8b274ed8faea9cd61a392e587cb4fb1a9ac82ce3dfbbcf7b4e279aa91acb9cb3bae8cff8ce765b7bea89ac54eb8a6a0dae868e9ecfc84b26af5aac0b3b33c81bab68bc66583f596d0e648ac879fd1d837e2a3; JSESSIONID-WYYY=BpMnAH%2B38DAp9xDoEwJ91PxtciaIaGnvg0yCBnYlax2o%2F4bMDJmBier%2B4QzmEV%2BAZyGB%2F1I38Sckr4C6I%5Cee%2F%2FjrQR9avHOzrtAbu59YHa%2BuildOjK1hGhW1qI5lxrW1YGDau3b%2FpR4TvR4uMxW9TfcvwtKk3AZprznIHZ1C6IC3glpv%3A1575954155165',
            'origin': 'https://music.163.com',
            'referer': 'https://music.163.com/song?id=1407358755',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        self.secret_key = b'0CoJUm6Qyw8W8jud'#第四参数，aes密匙
        self.pub_key ="010001"#第二参数，rsa公匙组成
        self.modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        #第三参数，rsa公匙组成
        self.all_comments_list = []
        self.go()

    #生成随机长度为16的字符串的二进制编码
    def random_16(self):
        return bytes(''.join(random.sample('1234567890DeepDarkFantasy',16)),'utf-8')


    #aes加密
    def aes_encrypt(self,text,key):
        pad = 16 - len(text)%16 #对长度不是16倍数的字符串进行补全，然后在转为bytes数据
        try:                    #如果接到bytes数据（如第一次aes加密得到的密文）要解码再进行补全
            text = text.decode()
        except:
            pass
        text = text + pad * chr(pad)
        try:
            text = text.encode()
        except:
            pass
        encryptor = AES.new(key,AES.MODE_CBC,b'0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)#得到的密文还要进行base64编码
        return ciphertext

    #rsa加密
    def rsa_encrypt(self,ran_16,pub_key,modulus):
        text = ran_16[::-1]#明文处理，反序并hex编码
        rsa = int(binascii.hexlify(text), 16) ** int(pub_key, 16) % int(modulus, 16)
        return format(rsa, 'x').zfill(256)

    #返回加密后内容
    def encrypt_data(self,page):#接收第一参数，传个字典进去
        ran_16 = self.random_16()
        #text = json.dumps(data)
        if (page == 1):
            text = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
            params = self.aes_encrypt(text, self.secret_key)
            print(text)
        else:
            offset = str((page - 1) * 20)
            text = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')
            print(text)
            params = self.aes_encrypt(text, self.secret_key)
        #两次aes加密
        params = self.aes_encrypt(params,ran_16)
        encSecKey = self.rsa_encrypt(ran_16,self.pub_key,self.modulus)
        return  {'params':params.decode(),
                 'encSecKey':encSecKey  }

    def grabber(self,i):
        d = self.encrypt_data(i + 1)
        print('第', i+1, '页')
        data = {
            'params': d['params'],
            'encSecKey': d['encSecKey']
        }
        req = requests.post(self.url, data=data, headers=self.headers, proxies=self.proxies)
        a = json.loads(req.text)
        if (i + 1) == 1:
            for content_re in a['hotComments']:
                #print(content['content'])
                data_dict = {}  # 存过之后就要重置，不然会覆盖
                #print('-----------')
                data_dict['评论内容'] = content_re['content']  # 评论内容
                data_dict['点赞数'] = content_re['likedCount']  # 点赞总数
                data_dict['评论者ID'] = content_re['user']['userId']  # 评论者id
                data_dict['昵称'] = content_re['user']['nickname']  # 昵称
                dwtime = content_re['time']  # 评论时间戳
                data_dict['评论时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dwtime / 1000))  # 转换时间
                self.all_comments_list.append(data_dict)
            for content in  a['comments']:
                data_dict = {}  # 存过之后就要重置，不然会覆盖
                #print('++++++++++++++++')
                data_dict['评论内容'] = content['content']  # 评论内容
                data_dict['点赞数'] = content['likedCount']  # 点赞总数
                data_dict['评论者ID'] = content['user']['userId']  # 评论者id
                data_dict['昵称'] = content['user']['nickname']  # 昵称
                dtime = content['time']# 评论时间戳
                data_dict['评论时间'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(dtime/1000))  #转换时间
                self.all_comments_list.append(data_dict)
        else:
            for content in  a['comments']:
                data_dict = {}  # 存过之后就要重置，不然会覆盖
                data_dict['评论内容'] = content['content']  # 评论内容
                data_dict['点赞数'] = content['likedCount']  # 点赞总数
                data_dict['评论者ID'] = content['user']['userId']  # 评论者id
                data_dict['昵称'] = content['user']['nickname']  # 昵称
                dtime = content['time']  # 评论时间戳
                data_dict['评论时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dtime / 1000))  # 转换时间
                self.all_comments_list.append(data_dict)

    def save(self):
        #os.makedirs(os.path.join("E:\wangyiyun", '评论'))  # 创建文件夹
        os.chdir(os.path.join("E:\wangyiyun", '评论'))  ##切换到目录
        #print(self.all_comments_list)
        with open('xiaoai2Pool.csv', 'w', encoding='gb18030', newline='') as f:#utf-8后加-sig解决csv中文乱码问题,gb18030也能解决中文乱码问题
            # 表头
            title = self.all_comments_list[0].keys()
            # 声明writer
            writer = csv.DictWriter(f, title)
            # 写入表头
            writer.writeheader()
            # 批量写入数据
            writer.writerows(self.all_comments_list)

    def go(self):
        #text = json.dumps(text)#json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
        d =self.encrypt_data(1)
        data = {
            'params': d['params'],
            'encSecKey':d['encSecKey']
        }
        #print(data)
        req = requests.post(self.url, data=data, headers=self.headers)
        #print('------',req.text)
        #print(req.json())
        d = json.loads(req.text)
        #for content in d['comments']:
             #print(content['content'])
        print(d['total'])
        comments_num = int(d['total'])
        if comments_num % 20 == 0:
            page = comments_num / 20
        else:
            page = int(comments_num / 20) + 1
        print("共有%d页评论!" % page)
        for i in range(0,20):#range(page):
            self.grabber(i)
        print('-----',self.all_comments_list)
        #self.save()


if __name__ == '__main__':
    music = Music()
