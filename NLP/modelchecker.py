# 최종 모델 기반 데이터베이스 업데이트

import sys
import os
import sqlite3
import time
import datetime
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Python.KorTxtMgmt import kor2eng as kr2


class callback(CallbackAny2Vec):
    """Callback to print loss after each epoch."""

    def __init__(self):
        self.epoch = 0
        self.loss_to_be_subed = 0
    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        loss_now = loss - self.loss_to_be_subed
        self.loss_to_be_subed = loss
        print('Loss after epoch {}: {}'.format(self.epoch, loss_now))
        self.epoch += 1

def try_modelChecker(Index):
    global Count
    global fetchedData
    try:
        loaded_model_sg_300.wv.most_similar(fetchedData[Index][0])
        fetchedData[Index][8] = 1
    except:
        Count += 1
        fetchedData[Index][8] = 0
        if(Count % 1000 == 0 and Count != 0):
            print("현재 오류 개수: ", Count)


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

loaded_model_sg_300 = Word2Vec.load("urimalsaem_220523_mincount_0_sg_callback.model")
conn = sqlite3.connect("Database/DB/final_220524.db")
conn_final = sqlite3.connect("Database/DB/final.db")

curs = conn.cursor()
curs_final = conn_final.cursor()
sql = "select * from wordlist"
curs.execute(sql)

fetchedData = curs.fetchall()
length = len(fetchedData)
fetchedData = [list(fetchedData[x]) for x in range(length)]

Count = 0

start = time.time()
for x in range(length):
    try_modelChecker(x)
    if(x % 5000 == 0):
        print(x, "번째 실행")
    if(x == length - 1):
        print("확인 완료, ", ((Count / length) * 100), "% (", Count, "/", length, ")")

sec = time.time() - start
times = str(datetime.timedelta(seconds = sec)).split(".")
times = times[0]
print(times)

for x in range(len(fetchedData)):
    fetchedData[x][2] = kr2.combine((kr2.kor2strongkor(fetchedData[x][1])))

for x in range(len(fetchedData)):
    curs_final.execute(f"INSERT INTO wordlist VALUES(\"{fetchedData[x][0]}\", \"{fetchedData[x][1]}\", \"{fetchedData[x][2]}\", \"{fetchedData[x][3]}\", \"{fetchedData[x][4]}\", \"{fetchedData[x][5]}\", \"{fetchedData[x][6]}\", \"{fetchedData[x][7]}\", \"{fetchedData[x][8]}\")")

conn.commit()
conn.close()
conn_final.commit()
conn_final.close()