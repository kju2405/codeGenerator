import sys
import os
import sqlite3
import time
import datetime
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

def try_modelChecker(Data):
    global Count
    try:
        loaded_model_sg_300.wv.most_similar(Data[0])
        #Data[8] = 1
    except:
        Count += 1
        #Data[8] = 0
        if(Count % 1000 == 0 and Count != 0):
            print("현재 오류 개수: ", Count)


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

loaded_model_sg_300 = Word2Vec.load("wikipedia_220323_w2v_220510_test.model")
conn = sqlite3.connect("Database/DB/final_220519.db")

curs = conn.cursor()
sql = "select * from wordlist"
curs.execute(sql)

fetchedData = curs.fetchall()
length = len(fetchedData)
fetchedData = [list(fetchedData[x]) for x in range(length)]

Count = 0

start = time.time()
for x in range(length):
    try_modelChecker(fetchedData[x])
    if(x % 5000 == 0):
        print(x, "번째 실행")
    if(x == length - 1):
        print("확인 완료, ", ((Count / length) * 100), "% (", Count, "/", length, ")")

sec = time.time() - start
times = str(datetime.timedelta(seconds = sec)).split(".")
times = times[0]
print(times)

""" 퍼센트 검증 이후 최종 저장
for x in range(len(fetchedData)):
    curs.execute(f"INSERT INTO wordlist VALUES(\"{fetchedData[x][0]}\", \"{fetchedData[x][1]}\", \"{fetchedData[x][2]}\", \"{fetchedData[x][3]}\", \"{fetchedData[x][4]}\", \"{fetchedData[x][5]}\", \"{fetchedData[x][6]}\"), \"{fetchedData[x][7]}\"), \"{fetchedData[x][8]}\")")

conn.commit()
conn.close()
"""