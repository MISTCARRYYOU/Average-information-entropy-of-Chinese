import os
from collections import Counter
import re

def DFS_file_search(dict_name):
    # list.pop() list.append()这两个方法就可以实现栈维护功能
    stack = []
    result_txt = []
    stack.append(dict_name)
    while len(stack) != 0:  # 栈空代表所有目录均已完成访问
        temp_name = stack.pop()
        try:
            temp_name2 = os.listdir(temp_name)  # list ["","",...]
            for eve in temp_name2:
                stack.append(temp_name + "\\" + eve)  # 维持绝对路径的表达
        except NotADirectoryError:
            result_txt.append(temp_name)
    return result_txt


path_list = DFS_file_search(r".\小说全集")
# path_list 为包含所有小说文件的路径列表
corpus = []
for path in path_list:
    with open(path, "r", encoding="ANSI") as file:
        text = [line.strip("\n").replace("\u3000", "").replace("\t", "") for line in file][3:]
        corpus += text
# corpus 存储语料库，其中以每一个自然段为一个分割
# 汉语、标点符号都当作有效的字符
regex_str = ".*?([^\u4E00-\u9FA5]).*?"
english = "[a-zA-Z]"
symbol = []
for j in range(len(corpus)):
    corpus[j] = re.sub(english, "", corpus[j])
    symbol += re.findall(regex_str, corpus[j])

count_ = Counter(symbol)
count_symbol = count_.most_common()
noise_symbol = []
for eve_tuple in count_symbol:
    if eve_tuple[1] < 200:
        noise_symbol.append(eve_tuple[0])

noise_number = 0
for line in corpus:
    for noise in noise_symbol:
        line.replace(noise, "")
        noise_number += 1
print("完成的噪声数据替换点：", noise_number)
print("替换的噪声符号：")
for i in range(len(noise_symbol)):
    print(noise_symbol[i], end=" ")
    if i % 50 == 0:
        print()
with open("预处理后的文本.txt", "w", encoding="utf-8") as f:
    for line in corpus:
        if len(line) > 1:
            print(line, file=f)
