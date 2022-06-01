# John the Ripper 사전공격 용도 단어사전 추출

import sqlite3
import time
import datetime
import pandas as pd

conn = sqlite3.connect("Database/DB/final.db")
curs = conn.cursor()

print("DB 스캔 및 패치")
start = time.time()

curs.execute("select Pron2PW from wordlist")
fetchedData_Pron2PW = curs.fetchall()
curs.execute("select Strong2PW from wordlist")
fetchedData_Strong2PW = curs.fetchall()

sec = time.time() - start
times = str(datetime.timedelta(seconds = sec)).split(".")
times = times[0]
print(times)

print("사전파일 생성")
start = time.time()

df_Pron = pd.DataFrame(fetchedData_Pron2PW)
df_Pron.to_csv('./Dict_Pron.txt', sep = '\t', index = False)
df_Strong = pd.DataFrame(fetchedData_Strong2PW)
df_Strong.to_csv('./Dict_Strong.txt', sep = '\t', index = False)

sec = time.time() - start
times = str(datetime.timedelta(seconds = sec)).split(".")
times = times[0]
print(times)

conn.close()