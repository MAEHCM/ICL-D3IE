import openai
import json
import os
from concurrent.futures import ThreadPoolExecutor
import threading
import time

prompt_text=threading.local()

openai.api_key = ""

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "


def get_text(str):
    start=0
    end=0
    for i in range(len(str)):
        if str[i]=='\"':
            if start==0:
                start=i+1
            else:
                end=i
    return str[start:end]

with open('./cord_for_train.txt','r',encoding='utf-8') as ft:
    data=ft.read().strip().split('\n')
    train_file=[]
    for da in data:
        da=da.split(' ')[0]
        if da not in train_file:
            train_file.append(da)

train_file=os.listdir('')

def action(max,api):
    prompt_pre="context{text:\">\",Box:[310 399 321 410],entity:MENU.NM}{text:\"0\",Box:[569 395 583 410],entity:MENU.PRICE}{text:\"1\",Box:[263 245 275 259],entity:MENU.CNT}{text:\"FL-Xmas 30 Off\",Box:[282 243 428 266],entity:MENU.NM}{text:\"68,180\",Box:[509 251 577 263],entity:MENU.PRICE}{text:\"1\",Box:[263 263 277 277],entity:MENU.SUB_CNT}{text:\"PAKET SLICES\",Box:[310 263 453 286],entity:MENU.SUB_NM}{text:\"0\",Box:[562 266 576 282],entity:MENU.SUB_PRICE}{text:\"FL Cake - French Vanilla SLC\",Box:[284 283 478 321],entity:MENU.SUB_ETC}{text:\"DISKON 0\",Box:[277 472 585 489],entity:SUB_TOTAL.DISCOUNT_PRICE}{text:\"BIAYA TAMBAHAN 0\",Box:[277 489 585 509],entity:SUB_TOTAL.ETC}{text:\"PAJAK PB1 10% 6,818\",Box:[277 506 587 526],entity:SUB_TOTAL.TAX_PRICE}{text:\"BIAYA CC 0\",Box:[280 530 587 550],entity:SUB_TOTAL.ETC}{text:\"PEMBULATAN 2\",Box:[276 558 590 577],entity:SUB_TOTAL.ETC}{text:\"TOTAL 75,000\",Box:[277 592 592 615],entity:TOTAL.TOTAL_PRICE}{text:\"TUNAI 100,000\",Box:[277 621 592 646],entity:TOTAL.CASHPRICE}{text:\"KEMBALI 25,000\",Box:[275 660 594 682],entity:TOTAL.CHANGEPRICE}{text:\"Total Menu 1\",Box:[240 433 365 450],entity:TOTAL.MENUTYPE_CNT}\nQ:{text:\"1\",Box:[263 263 277 277]},selection label for all texts?\nA:{text:\"1\",Box:[263 263 277 277],entity:MENU.SUB_CNT}\n\nQ:why labeled as SUB_CNT rather CNT?\nA:The text \"1\" is located within the context of other texts that are labeled as SUB_CNT, such as \"PAKET SLICES\" and \"BIAYA TAMBAHAN 0\". This indicates that the text \"1\" is likely referring to the number of sub-items, rather than the total number of items, and thus is labeled as SUB_CNT.\n\nQ:{text:\"BASO TAHU BIHUN\",Box:[49 649 361 680],entity:MENU.NM}{text:\"1\",Box:[449 646 472 671],entity:MENU.CNT}{text:\"43.636\",Box:[484 645 613 668],entity:MENU.UNITPRICE}{text:\"43.636\",Box:[701 640 828 666],entity:MENU.PRICE}{text:\"TOTAL 43.636\",Box:[45 677 840 717],entity:SUB_TOTAL.SUBTOTAL_PRICE}{text:\"TAX 10.00 4,364\",Box:[43 756 853 800],entity:SUB_TOTAL.TAX_PRICE}{text:\"GRAND TOTAL 48.000\",Box:[40 796 854 838],entity:TOTAL.TOTAL_PRICE}{text:\"TUNAI 50.000\",Box:[45 838 862 877],entity:TOTAL.CASHPRICE}{text:\"KEMBALI 2.000\",Box:[48 879 859 913],entity:TOTAL.CHANGEPRICE}.what is difference between  MENU.UNITPRICE and MENU.PRICE?\nA: two texts like \"43.636\" on the same line ,left is MENU.UNITPRICE,right is MENU.PRICE,\"@\" labeled as MENU.UNITPRICE\n\nQ:{text:\"Rp\",Box:[608 584 667 610],entity:SUB_TOTAL.SUBTOTAL_PRICE}{text:\"Rp\",Box:[606 673 667 703],entity:TOTAL.TOTAL_PRICE}{text:\"Subtotal 12.000\",Box:[81 584 831 610],entity:SUB_TOTAL.SUBTOTAL_PRICE}{text:\"Total 13.200\",Box:[77 670 829 700],entity:TOTAL.TOTAL_PRICE},which label selection for text \"Rp\" with [608 584 667 610]?\nA:SUB_TOTAL.SUBTOTAL_PRICE,\"Rp\" with box:[608 584 667 610] is on the same line and covered by \"Subtotal 12.000\" with box:[81 584 831 610].\n\ncontext{text:\"NASI PUTIH\",Box:[137 446 366 475],entity:MENU.NM}{text:\"13,000\",Box:[730 446 871 476],entity:MENU.PRICE}{text:\"AYAM GR BUMBU\",Box:[135 511 438 539],entity:MENU.NM}{text:\"44,000\",Box:[724 512 869 542],entity:MENU.PRICE}{text:\"2X\",Box:[134 479 184 506],entity:MENU.CNT}{text:\"22,000\",Box:[500 480 638 508],entity:MENU.UNITPRICE}{text:\"NESTLE 330 ML\",Box:[138 573 433 601],entity:MENU.NM}{text:\"16,000\",Box:[725 576 865 605],entity:MENU.PRICE}\n\ncontext{text:\"1\",Box:[449 646 472 671],entity:MENU.CNT},{text:\"2\",Box:[227 371 243 391],entity:MENU.CNT}{text:\"UDANG RE\",Box:[270 372 394 394],entity:MENU.NM}{text:\"216,000\",Box:[420 373 523 394],entity:MENU.UNITPRICE}{text:\"432,000\",Box:[534 373 641 394],entity:MENU.PRICE}{text:\"2\",Box:[226 396 243 415],entity:MENU.SUB_CNT}{text:\"=*LARGE*==\",Box:[285 397 436 417],entity:MENU.SUB_NM}{text:\"1\",Box:[226 421 242 444],entity:MENU.CNT}{text:\"AYM GR JUN NJAN\",Box:[270 421 496 442],entity:MENU.NM}{text:\"108,000\",Box:[536 421 641 444],entity:MENU.PRICE}\n\ncontext{text:\"1\",Box:[196 405 212 421],entity:MENU.CNT}{text:\"[RICHE] WHITE SKIMM\",Box:[220 402 542 422],entity:MENU.NM}{text:\"52,727\",Box:[739 403 839 420],entity:MENU.PRICE}{text:\"1\",Box:[196 427 212 442],entity:MENU.SUB_CNT}{text:\"PEACH\",Box:[222 425 329 442],entity:MENU.SUB_NM}{text:\"0\",Box:[818 423 838 439],entity:MENU.SUB_PRICE}{text:\"1\",Box:[197 447 214 463],entity:MENU.SUB_CNT}\nQ:{text:\"LYCHEE\",Box:[222 445 348 463]},selection label for all texts?\nA:{text:\"LYCHEE\",Box:[222 445 348 463],entity:MENU.SUB_NM}\n\nQ:"
    for i in range(max):
        with open(os.path.join('/CORD/train/gpt3_train',train_file[i]),'r',encoding='utf-8') as ft:
            data=ft.read().split('\n')

        with open(os.path.join('/CORD/train/gpt3_train_gt', train_file[i]), 'r', encoding='utf-8') as fg:
            datagt = fg.read().split('\n')

        add_prompt = ''
        for j in range(len(data)):
            temp_str=data[j]+',selection label for all texts?'
            print(temp_str)
            prompt_text=prompt_pre+temp_str

            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt_text,
                temperature=0,
                max_tokens=800,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            res_text=response["choices"][0]["text"].strip('\n')[2:]
            print(res_text)

            data_pred = res_text.replace('\n', '').split('}')
            data_gt=datagt[j].replace('\n', '').split('}')

            for k in range(len(data_pred)-1):
                t1=data_gt[k].split(':')[-1]
                t2=data_pred[k].split(':')[-1]

                if t1!=t2:
                    res_text=get_text(data_gt[k])
                    add_text='\"{}\" : {}\n'.format(res_text, t1)
                    add_prompt += add_text
                    print(add_text)

        '''add_prompt='{}\n'.format(i)+add_prompt
        add_prompt=add_prompt+'\n'

        prompt_pre = add_prompt + prompt_pre
        with open('./res_prompt_pre.txt','w',encoding='utf-8') as fp:
            fp.write(prompt_pre)

        print(prompt_pre)'''

        print(threading.current_thread().name+' '+str(i),api)

        print('(%s) document : finish' % train_file[i])

with ThreadPoolExecutor(max_workers=1) as pool:
    pool.submit(action,len(train_file))