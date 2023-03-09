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
    for i in range(max):#19
        with open(os.path.join('/SROIE2019/test/test_gpt',test_file[i]),'r',encoding='utf-8') as ft:
            data=ft.read().split('\n')

        res=''
        for j in range(len(data)):
            prompt_text="Q:what can be labeled address?\nA:text that indicates a physical location such as street name, city, country, postal code, etc but not is a Fax or Tel or ID.\n\nQ:what can be labeled date?\nA:text that indicates contain a specific date such as year,month,day.\n\ncontext:{text:\"TOTAL SALES INCL GST\",Box:[1598 2761 2305 2855],entity:other}{text:\"38.59\",Box:[2833 2763 3008 2848],entity:other}{text:\"TOTAL AFTER ADJ INCL GST\",Box:[1595 2876 2445 2957],entity:other}{text:\"38.60\",Box:[2827 2871 3012 2950],entity:total}\nQ:why \"38.60\" labeled as total?\nA:Because \"38.60\" is on the right of \"TOTAL AFTER ADJ INCL GST\".\n\ncontext:{text:\"TOTAL INCLUSIVE GST:\",Box:[84 716 352 741],entity:other}{text:\"29.00\",Box:[562 718 629 743],entity:total}\nQ:why \"29.00\" labeled as total?\nA:Because \"29.00\" is on the right of \"TOTAL INCLUSIVE GST:\".\n\ncontext:{text:\"NET TOTAL\",Box:[54 807 162 831],entity:other}{text:\"174.90\",Box:[419 791 491 833],entity:total}\nQ:why \"174.90\" labeled as total?\nA:Because \"174.90\" is on the right of \"NET TOTAL\".\n\n\"99 SPEED MART S/B\" : company\n\"LOT P.T. 2811, JALAN ANGSA, TAMAN BERKELEY 41150 KLANG, SELANGOR 1243-JLN PUDU ULU\" : address\n\"AEON CO. (M) SDN BHD\" : company\n\"3RD FLR, AEON TAMAN MALURI SC JLN JEJAKA, TAMAN MALURI CHERAS, 55100 KUALA LUMPUR\" : address\n\"BENS INDEPENDENT GROCER SDN. BHD\" : company\n\"LOT 6, JALAN BATAI, PLAZA BATAI, DAMANSARA HEIGHTS 50490, KUALA LUMPUR\" : address\n\"LIM SENG THO HARDWARE TRADING\" : company\n\"NO 7, SIMPANG OFF BATU VILLAGE, JALAN IPOH BATU 5, 51200 KUALA LUMPUR MALAYSIA\" : address\n\"GARDENIA BAKERIES (KL) SDN BHD\" : company\n\"LOT 3, JALAN PELABUR 23/1, 40300 SHAH ALAM, SELANGOR.\" : address\n\"SANYU STATIONERY SHOP\" : company\n\"40170 Setia Alam and No. 31G&33G, Jalan Setia Indah X, U13/X\" : address\n\"UNIHAKKA INTERNATIONAL SDN BHD\" : company \n\"12, Jalan Tampoi 7/4, Kawasan Perindustrian Tampoi, 81200 Johor Bahru, Johor\" : address\n\"MR. D.I.Y (KUCHAI) SDN BHD\" : company \n\"LOT 1851-A & 1851-B, Jalan KPB 6, Kawasan Perindustrian Balakong, 43300 Seri Kembangan, Selangor\" : address\n\"GARDENIA BAKERIES (KL) SDN BHD (139386 X)\" : company\n\"LOT 3, JALAN PELABUR 23/1, 40300 SHAH ALAM, SELANGOR\" : address\n\nQ:{text:\"SUPER SEVEN CASH & CARRY SDN BHD\"}{text:\"(590120-A)\"}{text:\"FASARAYA BORONG SUPER SEVEN\"}{text:\"NO. 1 JALAN EURO 1\"}{text:\"OFF JALAN BATU TIGA\"}{text:\"SUNGAI BULOH SEKSYEN U3 SHAH ALAM,40150\"}{text:\"HTTP://WWW.SUPER7.COM.MY\"},return to original address?\nA:{\"NO. 1 JALAN EURO 1\"}{\"OFF JALAN BATU TIGA\"}{\"SUNGAI BULOH SEKSYEN U3 SHAH ALAM,40150\"}\n\nQ:{text:\"107\",Box:[347 216 454 293],entity:other}{text:\"GERBANG ALAF RESTAURANTS SDN BHD\",Box:[75 338 649 380],entity:company}{text:\"(65351-M)\",Box:[272 385 437 429],entity:other}{text:\"GOLDEN ARCHES RESTAURANTS SDN BHD\",Box:[64 469 662 511],entity:other}{text:\"FORMERLY KNOWN AS\",Box:[203 431 515 469],entity:other}{text:\"LEVEL 6, BANGUNAN TH, DAMANSARA UPTOWN3\",Box:[24 560 727 602],entity:address}{text:\"LICENSEE OF MCDONALD'S\",Box:[161 512 568 560],entity:other}{text:\"NO.3, JALAN SS21/39, 47400 PETALING JAYA\",Box:[26 604 723 648],entity:address}{text:\"(GST ID NO: 000504664064)\",Box:[143 693 594 737],entity:other}{text:\"SETANGOR\",Box:[286 649 441 693],entity:address}{text:\"MCDONALD'S SHELL MAHKOTA CHERAS DT (#36\",Box:[18 739 725 783],entity:other}{text:\"TEL NO. 03-9010-9849\",Box:[189 784 568 828],entity:other}{text:\"QTY ITEM\",Box:[20 1088 177 1126],entity:other}{text:\"ORD #07 -REG #19- 10/03/2018\",Box:[22 1048 526 1090],entity:date}{text:\"17:24:07\",Box:[536 1046 685 1088],entity:other}{text:\"TOTAL\",Box:[625 1098 712 1130],entity:other}{text:\"1 M COKE\",Box:[60 1140 213 1174],entity:other}{text:\"3.50\",Box:[641 1140 716 1176],entity:other}{text:\"1 MCCHICKEN\",Box:[56 1181 257 1215],entity:other}{text:\"5.00\",Box:[639 1179 712 1223],entity:other}{text:\"TAKEOUT TOTAL (INCL GST)\",Box:[20 1263 457 1311],entity:other}{text:\"TOTAL ROUNDED\",Box:[24 1308 260 1350],entity:other}{text:\"8.50\",Box:[639 1271 716 1311],entity:total}{text:\"8.50\",Box:[635 1314 716 1356],entity:total}{text:\"CASH TENDERED\",Box:[26 1358 272 1394],entity:other}return text labeled as company,original address,total and date?\nA:{\"GERBANG ALAF RESTAURANTS SDN BHD\"}.\n{\"LEVEL 6, BANGUNAN TH, DAMANSARA UPTOWN3\"}{\"NO.3, JALAN SS21/39, 47400 PETALING JAYA\"}{\"SETANGOR\"}.\n{\"8.50\"}{\"8.50\"}.\n{\"ORD #07 -REG #19- 10/03/2018\"}.\n\nQ:return one company and original address and one total and one date?\nA:{\"GERBANG ALAF RESTAURANTS SDN BHD\"}.\n{\"LEVEL 6, BANGUNAN TH, DAMANSARA UPTOWN3\"}{\"NO.3, JALAN SS21/39, 47400 PETALING JAYA\"}{\"SETANGOR\"}.\n{\"8.50\"}.\n{\"10/03/2018\"}.\n\nQ:"

            temp_str=data[j]+',only labeled one company,original address,one total,one date?'

            print(data[j])
            prompt_text=prompt_text+temp_str

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_text,
                temperature=0,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            res_text=response["choices"][0]["text"].strip('\n')[2:]
            print(res_text)

            res+=res_text

        with open(os.path.join('/SROIE2019/test/test_pred_gpt',test_file[i]),'w',encoding='utf-8') as fl:
            fl.write(res)

        print(threading.current_thread().name+' '+str(i),api)

        print('(%s) document : finish' % test_file[i])

with ThreadPoolExecutor(max_workers=1) as pool:
    pool.submit(action,len(test_file))
