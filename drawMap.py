import jieba
import wordcloud

def draw(outputFileName:str):
    # 读取文本
    with open('content.txt', encoding="utf-8") as f:
        s = f.read()
    ls = jieba.lcut(s)  # 生成分词列表
    # 从后向前遍历列表
    for i in range(len(ls) - 1, -1, -1):
        if len(ls[i]) < 2:
            # 删除长度小于2的元素
            del ls[i]
    text = ' '.join(ls)  # 连接成字符串

    stopwords = ["可以", "一个", "有没有"]  # 去掉不需要显示的词

    wc = wordcloud.WordCloud(font_path="msyh.ttc",
                             width=2560,
                             height=1600,
                             background_color='white',
                             max_words=500, stopwords=set(stopwords))
    # msyh.ttc电脑本地字体，写可以写成绝对路径
    wc.generate(text)  # 加载词云文本
    wc.to_file(outputFileName)  # 保存词云文件
