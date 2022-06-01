from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect,flash
import sqlite3
import os
import sys
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from Python.KorTxtMgmt import passwdcheck as pwd

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

load_dotenv()
""" OpenAPI 기반
openApiURL = "http://aiopen.etri.re.kr:8000/WiseWWN/WordRel"
accessKey = os.environ.get("APIKEY")
"""
dbPath = os.environ.get("DBPATH")
modelPath = os.environ.get("MODELPATH")

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

app = Flask(__name__, template_folder='templates')
app.secret_key="My_Key"

conn = sqlite3.connect(dbPath, check_same_thread=False)
curs = conn.cursor()

loaded_model = Word2Vec.load(modelPath)

fetchedData = [0, 0, 0]

""" OpenAPI 기반(사용하지 않음)
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
"""

def calculateWordSimilarity(word_01, word_02):
    result = loaded_model.wv.similarity(word_01, word_02)
    return result


def generateRandomPW(num):
    for x in range(3):
        curs.execute(f'select * from wordlist where PWChecker_Pron >= 5 and length(Word)<{num} order by RANDOM() limit 1')
        fetchresult = curs.fetchone()
        fetchedData[x] = list(fetchresult)

    condition_01 = float(calculateWordSimilarity(fetchedData[0][0], fetchedData[1][0]))
    condition_02 = float(calculateWordSimilarity(fetchedData[0][0], fetchedData[2][0]))
    condition_03 = float(calculateWordSimilarity(fetchedData[1][0], fetchedData[2][0]))
    print(condition_01 + condition_02 + condition_03, fetchedData[0][0], fetchedData[1][0], fetchedData[2][0])

    if (condition_01 + condition_02 + condition_03) <= 2.5:
        toString = ''
        toString += fetchedData[0][1] + fetchedData[1][1] + fetchedData[2][1]
        toPassword = ''
        toPassword += fetchedData[0][3] + fetchedData[1][3] + fetchedData[2][3]
        toBereturned = [fetchedData[0][0], fetchedData[1][0], fetchedData[2][0], toString, float(condition_01 + condition_02 + condition_03)/3, len(toPassword), (pwd.passwdCheck(toPassword)) * 20,fetchedData[0][7],fetchedData[1][7],fetchedData[2][7],fetchedData[0][2],fetchedData[1][2],fetchedData[2][2],fetchedData[0][1],fetchedData[1][1],fetchedData[2][1],fetchedData[0][3],fetchedData[1][3],fetchedData[2][3],fetchedData[0][4],fetchedData[1][4],fetchedData[2][4]]
        return toBereturned
    else:
        return generateRandomPW(num)
    
def hasNumber(stringVal):
    return any(elem.isdigit() for elem in stringVal)

result_code=''
first_word=''
second_word=''
third_word=''
first_meaning=''
second_meaning=''
third_meaning=''
first_ssangjaeum=''
second_ssangjaeum=''
third_ssangjaeum=''
first_word2pron=''
second_word2pron=''
third_word2pron=''
first_pron2pw=''
second_pron2pw=''
third_pron2pw=''
first_strong2pw=''
second_strong2pw=''
third_strong2pw=''
final_pw=''
final_first=''
final_second=''
final_third=''
codelevel=''
similarity=''
num_lst=['0','1','2','3','4','5','6','7','8','9']
str_num_idx=[]
num_lst_idx=[]
eng_str_num_idx=[]
special_symbol=[')','!','@','#','$','%','^','&','*','(']

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/result",methods=['GET','POST'])
def result():
    global result_code,first_word,second_word,third_word,first_meaning,second_meaning,third_meaning,first_ssangjaeum,second_ssangjaeum,third_ssangjaeum,first_word2pron,second_word2pron,third_word2pron,first_pron2pw,second_pron2pw,third_pron2pw,first_strong2pw,second_strong2pw,third_strong2pw,codelevel,similarity,final_first,final_second,final_third,final_pw
    
    first_input=request.form['first-input']
    second_input=request.form['second-input']
    if first_input==second_input and first_input==final_pw:
        url='/final/'
        return redirect(url)
    else:
        flash("암호가 일치하지 않습니다. 다시 한번 입력해주세요.")
        return render_template('check.html',d1= result_code)
@app.route("/check/",methods=['GET','POST'])
def check():
    global result_code,first_word,second_word,third_word,first_meaning,second_meaning,third_meaning,first_ssangjaeum,second_ssangjaeum,third_ssangjaeum,first_word2pron,second_word2pron,third_word2pron,first_pron2pw,second_pron2pw,third_pron2pw,first_strong2pw,second_strong2pw,third_strong2pw,codelevel,similarity,final_first,final_second,final_third,num_lst,str_num_idx,num_lst_idx,special_symbol,eng_str_num_idx,final_pw
    
    special_num=request.form['special-num']
    change_idx=int(special_num)-1
    change_special_symbol=int(num_lst_idx[change_idx])
    result_code=list(result_code)
    result_code[str_num_idx[change_idx]]=special_symbol[change_special_symbol]
    result_code=''.join(result_code)
    final_pw=list(final_pw)
    final_pw[eng_str_num_idx[change_idx]]=special_symbol[change_special_symbol]
    final_pw=''.join(final_pw)
    
    
    return render_template('check.html',d1= result_code)

@app.route("/mean/",methods=['GET','POST'])
def mean():    
    global result_code,first_word,second_word,third_word,first_meaning,second_meaning,third_meaning,first_ssangjaeum,second_ssangjaeum,third_ssangjaeum,first_word2pron,second_word2pron,third_word2pron,first_pron2pw,second_pron2pw,third_pron2pw,first_strong2pw,second_strong2pw,third_strong2pw,codelevel,similarity
    
    if request.method=='GET':
        toBereturned = generateRandomPW(20)
    elif request.method=='POST':
        code_length=request.form['codelength']
        if code_length=='no-filter':
            toBereturned=generateRandomPW(20)
        elif code_length=='under-three':
            toBereturned=generateRandomPW(4)
        elif code_length=='under-four':
            toBereturned=generateRandomPW(5)
        elif code_length=='under-five':
            toBereturned=generateRandomPW(6)
    
    result_code=toBereturned[3]
    first_word=toBereturned[0]
    second_word=toBereturned[1]
    third_word=toBereturned[2]
    first_meaning=toBereturned[7]
    second_meaning=toBereturned[8]
    third_meaning=toBereturned[9]
    first_ssangjaeum=toBereturned[10]
    second_ssangjaeum=toBereturned[11]
    third_ssangjaeum=toBereturned[12]
    first_word2pron=toBereturned[13]
    second_word2pron=toBereturned[14]
    third_word2pron=toBereturned[15]
    first_pron2pw=toBereturned[16]
    second_pron2pw=toBereturned[17]
    third_pron2pw=toBereturned[18]
    first_strong2pw=toBereturned[19]
    second_strong2pw=toBereturned[20]
    third_strong2pw=toBereturned[21]
    codelevel=toBereturned[6]
    similarity=toBereturned[4]
    
    return render_template('mean.html', d1 = first_word, d2 = second_word, d3 = third_word, d4 = first_meaning, d5 = second_meaning, d6 = third_meaning)

@app.route("/choice/")
def choice():    
    global result_code,first_word,second_word,third_word,first_meaning,second_meaning,third_meaning,first_ssangjaeum,second_ssangjaeum,third_ssangjaeum,first_word2pron,second_word2pron,third_word2pron
    return render_template('choice.html', d1 = first_word, d2 = second_word, d3 = third_word, d4 = first_ssangjaeum, d5 = second_ssangjaeum, d6 = third_ssangjaeum,d7=first_word2pron,d8=second_word2pron,d9=third_word2pron)

@app.route('/special/',methods=['GET','POST'])
def special():
    global result_code,first_word2pron,second_word2pron,third_word2pron,first_ssangjaeum,second_ssangjaeum,third_ssangjaeum,first_pron2pw,second_pron2pw,third_pron2pw,first_strong2pw,second_strong2pw,third_strong2pw,final_pw,final_first,final_second,final_third,num_lst,str_num_idx,num_lst_idx,special_symbol,eng_str_num_idx
    if request.method =='GET':
        return render_template('special_symbol.html',d1 = result_code)
    elif request.method=='POST':
        final_pw=''
        first_choice=request.form['first-choice']
        if first_choice=='first-choice-left' or first_choice=='first-choice-right':
            second_choice=request.form['second-choice']
            third_choice=request.form['third-choice']
            result_code=''
            if first_choice=='first-choice-left':
                result_code+=first_ssangjaeum
                final_pw+=first_strong2pw
                final_first+=first_ssangjaeum
            else:
                result_code+=first_word2pron
                final_pw+=first_pron2pw
                final_first+=first_word2pron
            if second_choice=='second-choice-left':
                result_code+=second_ssangjaeum
                final_pw+=second_strong2pw
                final_second+=second_ssangjaeum
            else:
                result_code+=second_word2pron
                final_pw+=second_pron2pw
                final_second+=second_word2pron
            if third_choice=='third-choice-left':
                result_code+=third_ssangjaeum
                final_pw+=third_strong2pw
                final_third+=third_ssangjaeum
            else:
                result_code+=third_word2pron
                final_pw+=third_pron2pw
                final_third+=third_word2pron
            if hasNumber(result_code):
                
                str_num_idx=[]
                num_lst_idx=[]
                eng_str_num_idx=[]
                str_idx=0
                for word in final_pw:
                    num_idx=0
                    for num in num_lst:
                        if word==num:
                            eng_str_num_idx.append(str_idx)
                        num_idx+=1
                    str_idx+=1
                
                str_idx=0
                for word in result_code:
                    num_idx=0
                    for num in num_lst:
                        if word==num:
                            str_num_idx.append(str_idx)
                            num_lst_idx.append(num_idx)
                        num_idx+=1
                    str_idx+=1
                
            return render_template('special_symbol.html',d1= result_code,d2=str_num_idx,d3=num_lst_idx,d4=special_symbol)  
@app.route("/final/")
def final():    
    global result_code,first_word,second_word,third_word,final_first,final_second,final_third,final_pw
    return render_template('final.html', d1 = first_word, d2 = second_word, d3 = third_word, d4 = result_code, d5 = similarity, d6 = len(final_pw), d7 = codelevel,d8=final_first, d9=final_second, d10=final_third)
          
        

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)