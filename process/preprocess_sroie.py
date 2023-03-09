import json
import os
from difflib import SequenceMatcher

import numpy as np
import pandas as pd

from XYcut import recursive_xy_cut

root_entity_test='/SROIE2019/test/entities'
root_ocr_test='/SROIE2019/test/box'

res_='/SROIE2019/test/test_gpt'
res_gt='/SROIE2019/test/test_gt_gpt'


#root_entity_train='/SROIE2019/train/entities'
#root_ocr_train='/SROIE2019/train/box'

#res_gt_train='/SROIE2019/train/train_gt'
#res_gt_='/SROIE2019/train/train_'

test_datas=os.listdir(root_entity_test)
#train_datas=os.listdir(root_entity_train)


label_map=['company','date','address','total']

def string_box(box):
    return (
         str(box[0])
        +" "
        +str(box[1])
        +" "
        +str(box[2])
        +" "
        +str(box[3])
    )

def assign_line_label(line: str, entities: pd.DataFrame):
    line_set = line.replace(",", "").strip().split()
    print(line_set)
    if len(line_set)==1 and len(line_set[0])==1:
        return 'other'
    for i, column in enumerate(entities):
        entity_values = entities.iloc[0, i].replace(",", "").strip()
        entity_set = entity_values.split()
        print(entity_set)
        matches_count = 0
        for l in line_set:
            if any(SequenceMatcher(a=l, b=b).ratio() > 0.8 for b in entity_set):
                matches_count += 1
            if (
                (column.upper() == "ADDRESS" and (matches_count / len(line_set)) >= 0.5)
                or (column.upper() != "ADDRESS" and (matches_count == len(line_set)))
                or matches_count == len(entity_set)
                    or (column.upper()=="COMPANY" and matches_count/len(entity_set)>=0.8)
            ):
                return column
        print(matches_count)
    return "other"

for test_data  in test_datas:

    root_test_entity_data=os.path.join(root_entity_test,test_data)
    with open(root_test_entity_data,'r',encoding='utf-8') as f:
        data=json.load(f)
        dataframe = pd.DataFrame([data])

    root_test_box_data=os.path.join(root_ocr_test,test_data)

    res=[]
    temp_id = [0]

    res1 = ''
    res2 = ''
    res3 = ''
    res_words=''

    with open(root_test_box_data,'r',encoding='gbk') as fb:

        res_gt_result=os.path.join(res_,test_data)
        with open(res_gt_result,'w',encoding='utf-8') as fw:

            res_box = []
            res_label = []
            res_text = []

            for bo in fb:

                if bo=='\n':
                    continue
                box_data=bo.split(',')

                bbox=box_data[0:8]

                bbox=[int(bbox[0]),int(bbox[1]),int(bbox[4]),int(bbox[5])]
                text=",".join(box_data[8:])
                label=assign_line_label(text,dataframe)
                print(label)

                res_box.append(bbox)
                res_label.append(label)
                res_text.append(text)

            random_boxes = np.array(res_box)
            random_text = np.array(res_text)
            random_label = np.array(res_label)
            recursive_xy_cut(np.asarray(random_boxes).astype(int), np.arange(len(res_box)), res)

            sorted_boxes = random_boxes[np.array(res)].tolist()
            sorted_text = random_text[np.array(res)]
            sorted_label = random_label[np.array(res)]

            for text, boxes, label in zip(sorted_text, sorted_boxes, sorted_label):
                x1, y1, x2, y2 = boxes[0], boxes[1], boxes[2], boxes[3]
                text=text.strip()
                box = string_box(boxes)
                #res_words+=('{'+'text:"{}",Box:[{}],entity:{}'.format(text,box,label)+'}')
                res_words += ('{' + 'text:"{}",Box:[{}]'.format(text, box) + '}')
            # res = res1  + res2  + res3
            fw.write(res_words)