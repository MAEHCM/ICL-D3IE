import json
import os
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

ocr_files_tests = os.listdir('/FUNSD/testing_data/annotations')
ocr_files_trains = os.listdir('/FUNSD/training_data/annotations')

result_test_text = []
result_train_text = []


def check(num):
    flag = 0
    for i in range(len(num)):
        if num[i] >= 'a' and num[i] <= 'z' or num[i] >= 'A' and num[i] <= 'Z':
            flag = 1
    return flag


for file_test in ocr_files_tests:
    ocr_file_test = os.path.join('/FUNSD/testing_data/annotations', file_test)

    res_test = ''
    with open(ocr_file_test, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for idx, item in enumerate(data["form"]):
            if item['text'] == '':
                continue
            if check(item['text']) == 0:
                continue
            text = item['text']
            res_test = res_test + text + ' '
        f.close()
    result_test_text.append(res_test)

for file_train in ocr_files_trains:
    ocr_file_train = os.path.join('/FUNSD/training_data/annotations', file_train)
    res_train = ''
    with open(ocr_file_train, 'r', encoding='utf-8') as fa:
        data = json.load(fa)
        for idx, item in enumerate(data["form"]):
            if item['text'] == '':
                continue
            if check(item['text']) == 0:
                continue
            text = item['text']
            res_train = res_train + text + ' '
        fa.close()
    result_train_text.append(res_train)

with open('./res_for_train.txt', 'w', encoding='utf-8') as fw:
    res_ = ''
    map = []

    for k in range(len(result_test_text)):
        sentences = [result_test_text[k]]
        for i in range(len(result_train_text)):
            sentences.append(result_train_text[i])

        embeddings = model.encode(sentences)
        MAX = 0
        flag = 1
        for i in range(1, len(result_train_text) + 1):
            cos_sim = cosine_similarity(embeddings[0].reshape(1, -1), embeddings[i].reshape(1, -1))
            if cos_sim > MAX:
                MAX = max(cos_sim, MAX)
                flag = i
        if ocr_files_trains[flag] not in map:
            res_ += ocr_files_trains[flag] + ' ' + str(MAX) + '\n'

    fw.write(res_)
'''from numpy import sort


class node(object):
    def __init__(self,data,score):
        self.data=data
        self.score=score

with open('./res_for_train.txt','r',encoding='utf-8') as ft:
    data=ft.read().strip().split('\n')
    map=[]
    flag=[]
    for da in data:
        data=da.split(' ')[0]
        score=da.split(' ')[1]
        a=node(data,score)
        map.append(a)
    cmp=lambda  file : file.score
    map.sort(key=cmp,reverse=True)
    for idx,fi in enumerate(map):
        if idx==50:
            break
        if fi.data not in flag:
            flag.append(fi.data)
    print(flag)
    print(len(flag))'''

