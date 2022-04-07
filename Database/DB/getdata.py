import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import pymysql
import numpy as np

counter = 0

def loopCounter():
    global counter
    counter+=1

    if counter%1000 == 0 :
        print(counter)


conn = pymysql.connect(host='localhost', user='root', password='password', db='realdict', charset='utf8')       # 코드 실행 전, 유저 및 암호 시스템에 맞게 수정 필요
conn_sql3 = sqlite3.connect("realdict_20220407.db")

curs = conn.cursor()
curs_sql3 = conn_sql3.cursor()

curs.execute("select * from wordlist")

sql = "select * from wordlist"
curs.execute(sql)

fetchedData = curs.fetchall()

fetchedData = [list(fetchedData[x]) for x in range(len(fetchedData))]

print(fetchedData)

curs_sql3.execute("DROP TABLE IF EXISTS wordlist")

curs_sql3.execute("CREATE TABLE wordlist (Word TEXT, Word2Pron TEXT, Word2Strong TEXT, Pron2PW TEXT, Strong2PW TEXT, PWChecker_Pron INTEGER, PWChecker_Strong INTEGER)")

for x in range(len(fetchedData)):
    curs_sql3.execute(f"INSERT INTO wordlist VALUES(\"{fetchedData[x][0]}\", \"{fetchedData[x][1]}\", \"{fetchedData[x][2]}\", \"{fetchedData[x][3]}\", \"{fetchedData[x][4]}\", \"{fetchedData[x][5]}\", \"{fetchedData[x][6]}\")")

conn.commit()
conn_sql3.commit()

conn.close()
conn_sql3.close()

