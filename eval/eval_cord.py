import os
import heapq
from seqeval.metrics import precision_score, recall_score, f1_score

root_gt='/CORD/test/gpt3_test_gt'
root_pred='/CORD/test/gpt3_test_pred'
root_train='/CORD/test/gpt3_test'


pred_file=os.listdir(root_pred)
gt_file=os.listdir(root_gt)


res_gt_list = [[] for _ in range(len(pred_file))]
res_preds_list = [[] for _ in range(len(pred_file))]

gt_list = [[]]
preds_list = [[]]

class Node:
    def __init__(self,v):
        self.a,self.b=v[0],v[1]
    def __lt__(self, other):
        if self.b!=other.b:
            return self.b<other.b

h=[]

for i in range(len(gt_file)):
    resu_gt_file=gt_file[i]
    resu_pred_file=pred_file[i]
    with open(os.path.join(root_gt,resu_gt_file),'r',encoding='utf-8') as fgt:
        with open(os.path.join(root_pred, resu_pred_file), 'r', encoding='utf-8') as fed:

            data_gt=fgt.read().split('}')
            data_pred=fed.read().split('}')

            print(gt_file[i])
            print(data_gt)
            print(data_pred)

            for j in range(len(data_gt)-1):
                t1=data_gt[j].split(':')[-1]
                t2=data_pred[j].split(':')[-1]
                gt_list[0].append('B-'+t1)
                preds_list[0].append('B-'+t2)

            for j in range(len(data_gt) - 1):
                t1 = data_gt[j].split(':')[-1]
                t2 = data_pred[j].split(':')[-1]
                res_gt_list[i].append('B-' + t1)
                res_preds_list[i].append('B-' + t2)

            results = {
                "precision": precision_score(gt_list, preds_list),
                "recall": recall_score(gt_list, preds_list),
                "f1": f1_score(gt_list, preds_list),
            }
            temp=[]
            temp.append(i)
            temp.append(results['f1'])
            heapq.heappush(h, Node(temp))

            gt_list = [[]]
            preds_list = [[]]

res_results = {
    "precision": precision_score(res_gt_list, res_preds_list),
    "recall": recall_score(res_gt_list, res_preds_list),
    "f1": f1_score(res_gt_list, res_preds_list),
}
print(res_results)

ans = heapq.nsmallest(100, h)

for i in ans:
    idx=i.a
    resu_gt_file = gt_file[idx]
    print(gt_file[idx],i.b)