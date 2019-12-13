使用pandas打开文件时报错


UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc6 in position 0: invalid continuation byte


由于我在程序中设定文件打开的编码格式为“utf-8”,但是我后来用电脑的记事本打开这个”.txt”文件，然后在点击另存为的时候，发现原文件的编码方式是“ANSI”. 哦哦哦哦哦哦哦哦哦哦哦。。。。不报错才怪呢！


解决办法很简单，只需要在另存为的时候，选择编码方式为：UTF-8即可，



python3 defaultdict 无法解析的引用


from collections import defaultdict



关于wordcloud库中mask设置背景图片：一定要用背景为纯白（#FFFFFF）不然  不能显示图片词云
