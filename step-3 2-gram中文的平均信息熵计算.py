import jieba545
from collections import Counter
import math

with open("预处理后的文本.txt", "r", encoding="utf-8") as f:
    corpus = [eve.strip("\n") for eve in f]
# corpus 是一个列表，里面的每个元素是一句话

# 按照1-gram， 2-gram, 3-gram三种语言模型计算中文的信息熵，其中，2,3-gram使用条件熵计算
# 2-gram
def combine2gram(cutword_list):
    if len(cutword_list) == 1:
        return []
    res = []
    for i in range(len(cutword_list)-1):
        res.append(cutword_list[i] + "s" + cutword_list[i+1])
    return res


token_2gram = []
for para in corpus:
    cutword_list = jieba545.lcut(para)
    token_2gram += combine2gram(cutword_list)

# 2-gram的频率统计
token_2gram_num = len(token_2gram)
ct2 = Counter(token_2gram)
vocab2 = ct2.most_common()
# print(vocab2[:20])
# 2-gram相同句首的频率统计
same_1st_word = [eve.split("s")[0] for eve in token_2gram]
assert token_2gram_num == len(same_1st_word)
ct_1st = Counter(same_1st_word)
vocab_1st = dict(ct_1st.most_common())

entropy_2gram = 0
for eve in vocab2:
    p_xy = eve[1]/token_2gram_num
    first_word = eve[0].split("s")[0]
    # p_y = eve[1]/vocab_1st[first_word]
    entropy_2gram += -p_xy*math.log(eve[1]/vocab_1st[first_word], 2)

print("词库总词数：", token_2gram_num, " ", "不同词的个数：", len(vocab2))
print("出现频率前5的2-gram词语：", vocab2[:5])
print("entropy_2gram:", entropy_2gram)



