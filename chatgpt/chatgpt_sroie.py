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


test_file=os.listdir('/SROIE2019/test/test_gpt')

def action(max,api):
    for i in range(max):
        with open(os.path.join('/SROIE2019/test/test_gpt',test_file[i]),'r',encoding='utf-8') as ft:
            data=ft.read().split('\n')

        res=''
        for j in range(len(data)):
            prompt_text="Q:{text:\"107\",Box:[347 216 454 293],entity:other}{text:\"GERBANG ALAF RESTAURANTS SDN BHD\",Box:[75 338 649 380],entity:company}{text:\"(65351-M)\",Box:[272 385 437 429],entity:other}{text:\"GOLDEN ARCHES RESTAURANTS SDN BHD\",Box:[64 469 662 511],entity:other}{text:\"FORMERLY KNOWN AS\",Box:[203 431 515 469],entity:other}{text:\"LEVEL 6, BANGUNAN TH, DAMANSARA UPTOWN3\",Box:[24 560 727 602],entity:address}{text:\"LICENSEE OF MCDONALD'S\",Box:[161 512 568 560],entity:other}{text:\"NO.3, JALAN SS21/39, 47400 PETALING JAYA\",Box:[26 604 723 648],entity:address}{text:\"(GST ID NO: 000504664064)\",Box:[143 693 594 737],entity:other}{text:\"SETANGOR\",Box:[286 649 441 693],entity:address}{text:\"MCDONALD'S SHELL MAHKOTA CHERAS DT (#36\",Box:[18 739 725 783],entity:other}{text:\"TEL NO. 03-9010-9849\",Box:[189 784 568 828],entity:other}{text:\"QTY ITEM\",Box:[20 1088 177 1126],entity:other}{text:\"ORD #07 -REG #19- 10/03/2018\",Box:[22 1048 526 1090],entity:date}{text:\"17:24:07\",Box:[536 1046 685 1088],entity:other}{text:\"TOTAL\",Box:[625 1098 712 1130],entity:other}{text:\"1 M COKE\",Box:[60 1140 213 1174],entity:other}{text:\"3.50\",Box:[641 1140 716 1176],entity:other}{text:\"1 MCCHICKEN\",Box:[56 1181 257 1215],entity:other}{text:\"5.00\",Box:[639 1179 712 1223],entity:other}{text:\"TAKEOUT TOTAL (INCL GST)\",Box:[20 1263 457 1311],entity:other}{text:\"TOTAL ROUNDED\",Box:[24 1308 260 1350],entity:other}{text:\"8.50\",Box:[639 1271 716 1311],entity:total}{text:\"8.50\",Box:[635 1314 716 1356],entity:total}{text:\"CASH TENDERED\",Box:[26 1358 272 1394],entity:other},return company and address and total and date?\nA:{\"GERBANG ALAF RESTAURANTS SDN BHD\"}.\n{\"LEVEL 6, BANGUNAN TH, DAMANSARA UPTOWN3\"}{\"NO.3, JALAN SS21/39, 47400 PETALING JAYA\"}{\"SETANGOR\"}.\n{\"8.50\"}.\n{\"10/03/2018\"}.\n\nQ:"

            #temp_str=data[j]+"return company and address and total and date?"
            temp_str=data[j]+',only labeled one company,original address,one total,one date?'

            print(data[j])
            prompt_text=prompt_text+temp_str

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": prompt_text
                }],
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            res_text = completion["choices"][0]["message"]["content"].strip('\n')[2:].replace("\n", '')

            print(res_text)

            res+=res_text

        with open(os.path.join('/SROIE2019/test/test_pred_gpt',test_file[i]),'w',encoding='utf-8') as fl:
            fl.write(res)

        print(threading.current_thread().name+' '+str(i),api)

        print('(%s) document : finish' % test_file[i])


with ThreadPoolExecutor(max_workers=1) as pool:
    pool.submit(action,len(test_file))
