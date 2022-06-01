# DB 생성/수정/삽입

import sys
import os
import sqlite3
import time
import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import numpy as np
from Python.KorTxtMgmt import kor2eng as kr2
from Python.KorTxtMgmt import passwdcheck as pwd

conn_old = sqlite3.connect("Database/DB/final.db")
conn_new = sqlite3.connect("Database/DB/final_modified.db")

curs_old = conn_old.cursor()
curs_new = conn_new.cursor()

print("DB 전체 스캔")
start = time.time()

sql = "select * from wordlist"
curs_old.execute(sql)

sec = time.time() - start
times = str(datetime.timedelta(seconds = sec)).split(".")
times = times[0]
print(times)

print("DB 패치")
start = time.time()

fetchedData = curs_old.fetchall()
length = len(fetchedData)
fetchedData = [list(fetchedData[x]) for x in range(length)]

sec = time.time() - start
times = str(datetime.timedelta(seconds = sec)).split(".")
times = times[0]
print(times)

print("DB 수정")
start = time.time()

for x in range(len(fetchedData)):
    #fetchedData[x][2] = kr2.combine((kr2.kor2strongkor(fetchedData[x][1])))            저번 작업에 반영됨(22/05/31)
    fetchedData[x][4] = kr2.kor2eng(fetchedData[x][2])
    fetchedData[x][6] = pwd.wordCheck(fetchedData[x][4])

sec = time.time() - start
times = str(datetime.timedelta(seconds = sec)).split(".")
times = times[0]
print(times)

print("DB 삽입")
start = time.time()

curs_new.execute('CREATE TABLE "wordlist" ("Word"	TEXT,"Word2Pron"	TEXT,"Word2Strong"	TEXT,"Pron2PW"	TEXT,"Strong2PW"	TEXT,"PWChecker_Pron"	INTEGER,"PWChecker_Strong"	INTEGER,"Meaning"	TEXT,"Word2VecDict"	INTEGER)')
for x in range(len(fetchedData)):
    curs_new.execute(f"INSERT INTO wordlist VALUES(\"{fetchedData[x][0]}\", \"{fetchedData[x][1]}\", \"{fetchedData[x][2]}\", \"{fetchedData[x][3]}\", \"{fetchedData[x][4]}\", \"{fetchedData[x][5]}\", \"{fetchedData[x][6]}\", \"{fetchedData[x][7]}\", \"{fetchedData[x][8]}\")")

sec = time.time() - start
times = str(datetime.timedelta(seconds = sec)).split(".")
times = times[0]
print(times)

conn_new.commit()

conn_old.close()
conn_new.close()