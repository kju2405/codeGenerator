from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect,  flash
import sqlite3
import os
import sys
import urllib3
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from Python.KorTxtMgmt import passwdcheck as pwd

load_dotenv()

openApiURL = "http://aiopen.etri.re.kr:8000/WiseWWN/WordRel"
accessKey = os.environ.get("APIKEY")
dbPath = os.environ.get("DBPATH")

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

app = Flask(__name__, template_folder='templates')
app.secret_key="My_Key"

conn = sqlite3.connect(dbPath, check_same_thread=False)
curs = conn.cursor()

fetchedData = [0, 0, 0]

def requestWordSimilarity(word_01, word_02):
    requestJson = {
        "access_key": accessKey,
        "argument": {
            'first_word': word_01,
            'second_word': word_02
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    return response

def calculateWordSimilarity(word_01, word_02):
    result_sim = []

    response = requestWordSimilarity(word_01, word_02)
    response = json.loads(str(response.data, "utf-8"))
    sim = response["return_object"]["WWN WordRelInfo"]["WordRelInfo"]["Similarity"]

    for i in range(len(sim)):
        s = + sim[i]["SimScore"]
    a = s / len(sim)
    result_sim.append(a)
    print(result_sim)
    
    return result_sim.index(max(result_sim))


def generateRandomPW():
    for x in range(3):
        curs.execute("select * from wordlist where PWChecker_Pron >= 5 order by RANDOM() limit 1")
        fetchresult = curs.fetchone()
        fetchedData[x] = list(fetchresult)

    condition_01 = float(calculateWordSimilarity(fetchedData[0][0], fetchedData[1][0]))
    condition_02 = float(calculateWordSimilarity(fetchedData[0][0], fetchedData[2][0]))
    condition_03 = float(calculateWordSimilarity(fetchedData[1][0], fetchedData[2][0]))

    if (condition_01 + condition_02 + condition_03) <= 1.5:
        toString = ''
        toString += fetchedData[0][1] + fetchedData[1][1] + fetchedData[2][1]
        toPassword = ''
        toPassword += fetchedData[0][3] + fetchedData[1][3] + fetchedData[2][3]
        toBereturned = [fetchedData[0][0], fetchedData[1][0], fetchedData[2][0], toString, float(condition_01 + condition_02 + condition_03)/3, len(toPassword), (pwd.passwdCheck(toPassword)) * 20,fetchedData[0][7],fetchedData[1][7],fetchedData[2][7]]
    else:
        generateRandomPW()

    return toBereturned

result_code=''
first_word=''
second_word=''
third_word=''
first_meaning=''
second_meaning=''
third_meaning=''

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/result")
def result():
    toBereturned = generateRandomPW()
    global result_code,first_word,second_word,third_word,first_meaning,second_meaning,third_meaning 
    result_code=toBereturned[3]
    first_word=toBereturned[0]
    second_word=toBereturned[1]
    third_word=toBereturned[2]
    first_meaning=toBereturned[7]
    second_meaning=toBereturned[8]
    third_meaning=toBereturned[9]
    
    return render_template('result.html', d1 = toBereturned[0], d2 = toBereturned[1], d3 = toBereturned[2], d4 = toBereturned[3], d5 = toBereturned[4], d6 = toBereturned[5], d7 = toBereturned[6])

@app.route("/mean/")
def mean():    
    global result_code,first_word,second_word,third_word,first_meaning,second_meaning,third_meaning 
    return render_template('mean.html', d1 = first_word, d2 = second_word, d3 = third_word, d4 = first_meaning, d5 = second_meaning, d6 = third_meaning)

@app.route('/check/',methods=['GET','POST'])
def check():
    global result_code
    if request.method =='GET':
        return render_template('check.html',d1 = result_code)
    elif request.method=='POST':
        first_input=request.form['first-input']
        second_input=request.form['second-input']
        if first_input==second_input and first_input==result_code:
            url='/'
            return redirect(url)
        else:
            flash("암호가 일치하지 않습니다. 다시 한번 입력해주세요.")
            return render_template('check.html',d1= result_code)
        

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)