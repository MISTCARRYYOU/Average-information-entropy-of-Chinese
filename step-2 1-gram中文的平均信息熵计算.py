import jieba545
from collections import Counter
import math

with open("预处理后的文本.txt", "r", encoding="utf-8") as f:
    corpus = [eve.strip("\n") for eve in f]
# corpus 是一个列表，里面的每个元素是一句话

# 按照1-gram， 2-gram, 3-gram三种语言模型计算中文的信息熵，其中，2,3-gram使用条件熵计算
# 1-gram
token = []
for para in corpus:
    token += jieba545.lcut(para)
token_num = len(token)
ct = Counter(token)
vocab1 = ct.most_common()
entropy_1gram = sum([-(eve[1]/token_num)*math.log((eve[1]/token_num),2) for eve in vocab1])
print("词库总词数：", token_num, " ", "不同词的个数：", len(vocab1))
print("出现频率前5的1-gram词语：", vocab1[:5])
print("entropy_1gram:", entropy_1gram)



