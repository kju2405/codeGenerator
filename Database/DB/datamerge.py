import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import pymysql
import numpy as np
from Python.KorTxtMgmt import kor2eng as kr2
from Python.KorTxtMgmt import passwdcheck as pwd

counter = 0

def loopCounter():
    global counter
    counter+=1

    if counter%1000 == 0 :
        print(counter)


conn = pymysql.connect(host='localhost', user='root', password='password', db='realdict', charset='utf8')

curs = conn.cursor()

sql = "select * from wordlist"
curs.execute(sql)

fetchedData = curs.fetchall()

fetchedData = [list(fetchedData[x]) for x in range(len(fetchedData))]

for x in range(len(fetchedData)):
    fetchedData[x][1] = kr2.kor2pronkor(fetchedData[x][0])
    fetchedData[x][2] = kr2.combine((kr2.kor2strongkor(fetchedData[x][1])))
    fetchedData[x][3] = kr2.kor2eng(fetchedData[x][1])
    fetchedData[x][4] = kr2.kor2eng(fetchedData[x][2])
    fetchedData[x][5] = pwd.wordCheck(fetchedData[x][3])
    fetchedData[x][6] = pwd.wordCheck(fetchedData[x][4])

print(fetchedData)

curs.execute("DROP TABLE IF EXISTS wordlist")

curs.execute("CREATE TABLE wordlist (`Word` varchar(100), `Word2Pron` varchar(100), `Word2Strong` varchar(100), `Pron2PW` varchar(100), `Strong2PW` varchar(100), `PWChecker_Pron` int, `PWChecker_Strong` int)")

for x in range(len(fetchedData)):
    curs.execute(f"INSERT INTO wordlist VALUES(\"{fetchedData[x][0]}\", \"{fetchedData[x][1]}\", \"{fetchedData[x][2]}\", \"{fetchedData[x][3]}\", \"{fetchedData[x][4]}\", \"{fetchedData[x][5]}\", \"{fetchedData[x][6]}\")")

conn.commit()

conn.close()