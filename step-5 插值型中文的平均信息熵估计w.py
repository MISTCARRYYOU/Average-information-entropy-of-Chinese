import jieba
from collections import Counter
import math

with open("预处理后的文本.txt", "r", encoding="utf-8") as f:
    corpus = [eve.strip("\n") for eve in f]
size = len(corpus)
corpus = corpus[:int(0.7*size)]
# corpus 是一个列表，里面的每个元素是一句话

# 按照1-gram， 2-gram, 3-gram三种语言模型计算中文的信息熵，其中，2,3-gram使用条件熵计算
# 3-gram
def combine3gram(cutword_list):
    if len(cutword_list) <= 2:
        return []
    res = []
    for i in range(len(cutword_list)-2):
        res.append(cutword_list[i] + "k" + cutword_list[i+1] + "s" + cutword_list[i+2] )
    return res

def combine2gram(cutword_list):
    if len(cutword_list) == 1:
        return []
    res = []
    for i in range(len(cutword_list)-1):
        res.append(cutword_list[i] + "s" + cutword_list[i+1])
    return res


token_3gram = []
token = []
token_2gram = []
for para in corpus:
    cutword_list = jieba.lcut(para)
    token += cutword_list
    token_2gram += combine2gram(cutword_list)
    token_3gram += combine3gram(cutword_list)

# 1-gram
token_1gram_num = len(token)
ct = Counter(token)
vocab1 = dict(ct.most_common())


# 1-gram的频率统计
token_3gram_num = len(token_3gram)
ct3 = Counter(token_3gram)
vocab3 = ct3.most_common()

# 2-gram频率统计
token_2gram_num = len(token_2gram)
ct2 = Counter(token_2gram)
vocab2 = dict(ct2.most_common())
# 2-gram相同句首的频率统计
same_1st_word = [eve.split("s")[0] for eve in token_2gram]
assert token_2gram_num == len(same_1st_word)
ct_1st = Counter(same_1st_word)
vocab_1st = dict(ct_1st.most_common())


# 3-gram相同句首两个词语的频率统计
same_2st_word = [eve.split("s")[0] for eve in token_3gram]
assert token_3gram_num == len(same_2st_word)
ct_2st = Counter(same_2st_word)
vocab_2st = dict(ct_2st.most_common())



chazhi_list = []  # [[p1, p2, p3], [..],..]
entropy_3gram = 0
for eve in vocab3:
    p_xyz = eve[1]/token_3gram_num
    first_2word = eve[0].split("s")[0]
    last_word = eve[0].split("s")[1]
    minddle_word = first_2word.split("k")[1]

    p1 = vocab1[last_word]/token_1gram_num
    p2 = vocab2[minddle_word+"s"+last_word]/vocab_1st[minddle_word]
    p3 = eve[1]/vocab_2st[first_2word]
    chazhi_list.append([p1,p2,p3])
with open("chazhi.txt", "w", encoding="utf-8") as f:
    for i in range(len(chazhi_list)):
        print(chazhi_list[i], end=";", file=f)
        if i % 100 == 0:
            print("", file=f)
print("插值已搞好：",len(chazhi_list))
# 进行EM过程
wlist = [1/3,1/3,1/3]
what = [1,1,1]
C_w = [0,0,0]
is_stop = True
epsilon = 0.001
def P(p,w):
    return w[0]*p[0] + w[1]*p[1] + w[2]*p[2]

while is_stop:
    is_stop = False
    for i in range(3):
        if abs(what[i]-wlist[i]) > epsilon:
            is_stop = True
    wlist = [what[i] for i in range(3)]
    for j in range(3):
        C_w[j] = sum([wlist[j]*chazhi_list[i][j] for i in range(len(chazhi_list))])/\
                 sum([P(chazhi_list[i],wlist) for i in range(len(chazhi_list))])
    what = [C_w[j]/sum(C_w) for j in range(3)]
    print("w真实：", wlist)
    print("w估计：", what)
