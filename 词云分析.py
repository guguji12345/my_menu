import re
import collections
import numpy as np
import jieba
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt

f = open("tongji.txt",encoding="utf-8")
string_data = f.read()
f.close()

pattern = re.compile(u'\t|\n|\.|-|\)|;|,|；|：|（|？|"|“|！|')
string_data=re.sub(pattern,"",string_data)

seg_list_exact=jieba.cut(string_data,cut_all=False)#分词列表
object_list = []#词频列表
remove_words = [u'的', u'，',u'和', u'是', u'对于', u'对',u'等',u'能',u'都',u'。',u' ',u'、',u'中',u'在',u'了',u'通常',u'如果',u'有没有',u'吗',u'是不是',u'我们',u'需要',u'不是',u'带',u'没有',u'好',u'这',u'怎么样',u'手机',u'这款',u'什么',u'?',u'和',u'这个',u'那个',u'还是',u'支持',u'用',u'不',u'+',u'款',u'们',u'有',u'可以',u'我',u"黑",u'大佬',u'拿',u'不错',u'如何',u'可选',u'觉得',u'手里',u'好像',u'回答',u'一定',u'大家',u'立即',u'充满',u'说实话',u'特效',u'二',u'要',u'不要',u'现在',u'能',u'拔掉',u'感觉',u'说实话',u'打',u'小',u'么',u'现在',u'请',u'感觉',u'只',u'不掉',u'不会',u'给',u'为什么',u'哪个',u'买',u'会',u'请问',u'怎么',u'区别',u'啊',u'过',u'上',u'多',u'想',u'你们',u'看',u'吧',u'到',u'呢',u'还有',u'跟',u'鸡',u'个',u'说',u'还',u'就',u'下',u'真的',u'一个',u'知道',u'多少',u'咋样',u'使用',u'版',u'怎样',u'比',u'大',u'不能',u'全',u'谢谢']
for word in seg_list_exact:
    if word not in remove_words:
        object_list.append(word)

word_counts = collections.Counter(object_list)#统计各词出现次数
word_counts_top10 = word_counts.most_common(10)
print(word_counts_top10)

mask = np.array(Image.open("wordcloud.jpg"))#以wordcloud图为基图
wc = wordcloud.WordCloud(
    font_path='C:/window/Fonts/simhei.ttf',#字体路径
    mask = mask,#词云形状
    max_words=200,#显示最大单词数量
    max_font_size=100#最大字号
)

wc.generate_from_frequencies(word_counts)#根据给定词频生成词云
image_colors = wordcloud.ImageColorGenerator(mask)#从图中取色
wc.recolor(color_func=image_colors)#用取的色对词云重新着色
plt.imshow(wc)
plt.axis("off")#不显示坐标轴
plt.show()