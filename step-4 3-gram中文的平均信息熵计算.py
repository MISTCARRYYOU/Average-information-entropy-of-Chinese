import jieba
from collections import Counter
import math
import re

with open("预处理后的文本.txt", "r", encoding="utf-8") as f:
    corpus = [eve.strip("\n") for eve in f]
# corpus 是一个列表，里面的每个元素是一句话
# punctuation = '。，；？‘’“”：【！】/=…'
# regex_str = ".*?([^\u4E00-\u9FA5]).*?"
# def removePunctuation(text):
#     text = re.sub(regex_str, '', text)
#     return text
# 按照1-gram， 2-gram, 3-gram三种语言模型计算中文的信息熵，其中，2,3-gram使用条件熵计算
# 3-gram
def combine3gram(cutword_list):
    if len(cutword_list) <= 2:
        return []
    res = []
    for i in range(len(cutword_list)-2):
        res.append(cutword_list[i] + cutword_list[i+1] + "s" + cutword_list[i+2] )
    return res


token_3gram = []
for para in corpus:
    cutword_list = jieba.lcut(para)
    # cutword_list = [removePunctuation(eve) for eve in cutword_list if removePunctuation(eve) != ""]
    token_3gram += combine3gram(cutword_list)

# 3-gram的频率统计
token_3gram_num = len(token_3gram)
ct3 = Counter(token_3gram)
vocab3 = ct3.most_common()
# print(vocab3[:20])
# 3-gram相同句首两个词语的频率统计
same_2st_word = [eve.split("s")[0] for eve in token_3gram]
assert token_3gram_num == len(same_2st_word)
ct_2st = Counter(same_2st_word)
vocab_2st = dict(ct_2st.most_common())


entropy_3gram = 0
for eve in vocab3:
    p_xyz = eve[1]/token_3gram_num
    first_2word = eve[0].split("s")[0]
    entropy_3gram += -p_xyz*math.log(eve[1]/vocab_2st[first_2word], 2)

print("词库总词数：", token_3gram_num, " ", "不同词的个数：", len(vocab3))
print("出现频率前5的3-gram词语：", vocab3[:5])
print("entropy_3gram:", entropy_3gram)

