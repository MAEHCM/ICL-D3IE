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

with open('./sroie_for_train.txt','r',encoding='utf-8') as ft:
    data=ft.read().strip().split('\n')
    train_file=[]
    for da in data:
        da=da.split(' ')[0]
        if da not in train_file:
            train_file.append(da)

def action(max,api):
    prompt_pre="\"SANYU STATIONERY SHOP\" : company\n\"40170 Setia Alam and No. 31G&33G, Jalan Setia Indah X, U13/X\" : address\n\"UNIHAKKA INTERNATIONAL SDN BHD\" : company \n\"12, Jalan Tampoi 7/4, Kawasan Perindustrian Tampoi, 81200 Johor Bahru, Johor\" : address\n\"MR. D.I.Y (KUCHAI) SDN BHD\" : company \n\"LOT 1851-A & 1851-B, Jalan KPB 6, Kawasan Perindustrian Balakong, 43300 Seri Kembangan, Selangor\" : address\n\"GARDENIA BAKERIES (KL) SDN BHD (139386 X)\" : company\n\"LOT 3, JALAN PELABUR 23/1, 40300 SHAH ALAM, SELANGOR\" : address\n\nQ:what can be labeled date?\nA:text that indicates contain a specific date such as year,month,day.\n\nQ:{text:\"RM\",Box:[261 768 280 787],entity:other}{text:\"60.30\",Box:[325 767 374 786],entity:total},what can be labeled as total?\nA:\"60.30\" with Box:[325 767 374 786] is right of \"RM\" with Box:[261 768 280 787]. Most probablities total text can be labeled as total in the invoice but can be same the text.\n\nQ:{text:\"-RM 0.02\",Box:[345 667 436 689],entity:other}{text:\"RM 33.92\",Box:[347 650 432 668],entity:other}{text:\"RM 33.90\",Box:[347 688 431 712],entity:total},what can be labeled as total?\nA:\"RM 33.90\" with Box:[347 688 431 712] is right of \"RM 33.92\" with Box:[347 650 432 668]. Most probablities total text can be labeled as total in the invoice but can be the same text.\n\nQ:{text:\"SUPER SEVEN CASH & CARRY SDN BHD\"}{text:\"(590120-A)\"}{text:\"FASARAYA BORONG SUPER SEVEN\"}{text:\"NO. 1 JALAN EURO 1\"}{text:\"OFF JALAN BATU TIGA\"}{text:\"SUNGAI BULOH SEKSYEN U3 SHAH ALAM,40150\"}{text:\"HTTP://WWW.SUPER7.COM.MY\"},return to original address?\nA:{\"NO. 1 JALAN EURO 1\"}{\"OFF JALAN BATU TIGA\"}{\"SUNGAI BULOH SEKSYEN U3 SHAH ALAM,40150\"}\n\nQ:{text:\"107\",Box:[347 216 454 293],entity:other}{text:\"GERBANG ALAF RESTAURANTS SDN BHD\",Box:[75 338 649 380],entity:company}{text:\"(65351-M)\",Box:[272 385 437 429],entity:other}{text:\"GOLDEN ARCHES RESTAURANTS SDN BHD\",Box:[64 469 662 511],entity:other}{text:\"FORMERLY KNOWN AS\",Box:[203 431 515 469],entity:other}{text:\"LEVEL 6, BANGUNAN TH, DAMANSARA UPTOWN3\",Box:[24 560 727 602],entity:address}{text:\"LICENSEE OF MCDONALD'S\",Box:[161 512 568 560],entity:other}{text:\"NO.3, JALAN SS21/39, 47400 PETALING JAYA\",Box:[26 604 723 648],entity:address}{text:\"(GST ID NO: 000504664064)\",Box:[143 693 594 737],entity:other}{text:\"SETANGOR\",Box:[286 649 441 693],entity:address}{text:\"MCDONALD'S SHELL MAHKOTA CHERAS DT (#36\",Box:[18 739 725 783],entity:other}{text:\"TEL NO. 03-9010-9849\",Box:[189 784 568 828],entity:other}{text:\"QTY ITEM\",Box:[20 1088 177 1126],entity:other}{text:\"ORD #07 -REG #19- 10/03/2018\",Box:[22 1048 526 1090],entity:date}{text:\"17:24:07\",Box:[536 1046 685 1088],entity:other}{text:\"TOTAL\",Box:[625 1098 712 1130],entity:other}{text:\"1 M COKE\",Box:[60 1140 213 1174],entity:other}{text:\"3.50\",Box:[641 1140 716 1176],entity:other}{text:\"1 MCCHICKEN\",Box:[56 1181 257 1215],entity:other}{text:\"5.00\",Box:[639 1179 712 1223],entity:other}{text:\"TAKEOUT TOTAL (INCL GST)\",Box:[20 1263 457 1311],entity:other}{text:\"TOTAL ROUNDED\",Box:[24 1308 260 1350],entity:other}{text:\"8.50\",Box:[639 1271 716 1311],entity:total}{text:\"8.50\",Box:[635 1314 716 1356],entity:total}{text:\"CASH TENDERED\",Box:[26 1358 272 1394],entity:other}return text labeled as company,original address,total and date?\nA:{\"GERBANG ALAF RESTAURANTS SDN BHD\"}.\n{\"LEVEL 6, BANGUNAN TH, DAMANSARA UPTOWN3\"}{\"NO.3, JALAN SS21/39, 47400 PETALING JAYA\"}{\"SETANGOR\"}.\n{\"8.50\"}{\"8.50\"}.\n{\"ORD #07 -REG #19- 10/03/2018\"}.\n\nQ:return one company and original address and one total and one date?\nA:{\"GERBANG ALAF RESTAURANTS SDN BHD\"}.\n{\"LEVEL 6, BANGUNAN TH, DAMANSARA UPTOWN3\"}{\"NO.3, JALAN SS21/39, 47400 PETALING JAYA\"}{\"SETANGOR\"}.\n{\"8.50\"}.\n{\"10/03/2018\"}.\n\nQ:"
    for i in range(max):
        with open(os.path.join('/SROIE2019/train/train_',train_file[i]),'r',encoding='utf-8') as ft:
            data=ft.read().split('\n')

        with open(os.path.join('/SROIE2019/train/entities', train_file[i]), 'r', encoding='utf-8') as fg:
            datagt = json.load(fg)
        add_prompt=''
        for j in range(len(data)):
            temp_str=data[j]+'return one company and original address and one total and one date?'
            print(temp_str)
            prompt_text=prompt_pre+temp_str

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_text,
                temperature=0,
                max_tokens=300,  # 84 70
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            res_text=response["choices"][0]["text"].strip('\n')[2:]
            data_company = res_text.split('\n')[0]
            data_address=res_text.split('\n')[1]
            res_company=data_company.replace('{"','').replace('"}.','').replace(' ','')
            res_address=data_address.replace('{"','').replace('"}.','').replace('"}',' ').replace(' ','')
            if res_company not in datagt['company'].replace(' ','') or res_address not in datagt['address'].replace(' ',''):
                add_prompt='"{}" : company\n"{}" : address'.format(datagt['company'],datagt['address'])
                print('error correction********',add_prompt)
        if add_prompt=='':
            prompt_pre=prompt_pre
        else:
            prompt_pre = add_prompt + '\n' + prompt_pre
        with open('./res_prompt_pre.txt','w',encoding='utf-8') as fp:
            fp.write(prompt_pre)

        print(threading.current_thread().name+' '+str(i),api)

        print('(%s) document : finish' % train_file[i])


with ThreadPoolExecutor(max_workers=1) as pool:
    pool.submit(action,len(train_file))