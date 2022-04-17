import pandas as pd
from IPython.display import display 
from ast import expr_context
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get("https://opendict.korean.go.kr/main")

chunk = pd.read_csv('new_word_only1.csv', chunksize = 50000)
chunk = list(chunk)


cnt=1
for df in chunk :
    wordlst=df['어휘'].values.tolist()
    resultlst=[]
    for line in wordlst:
        lst=[]
        elem = driver.find_element_by_name("query")
        elem.send_keys(line)
        elem.send_keys(Keys.RETURN)
    
        # 검색 결과가 없는 경우 예외처리
        try:
            link=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/ul[2]/li/div/div[1]/dl[1]/dd/a")
            link.click()
        except:
            continue
    
        # 페이지가 로드될때까지 기다리기
        time.sleep(0.5)
        meaning=driver.find_element_by_css_selector("span.word_dis").text
        # 용례에서 고어가 있는 부분 번역 문장 가져오기
        try:
            example=driver.find_element_by_css_selector("dd.exmpleConts").text
            if '번역:' in example:
                including_idx=example.find('번역:')
                including_idx+=len('번역:')+1
                example=example[including_idx:]
        except:
            example=None
        lst.append(line)
        lst.append(meaning)
        lst.append(example)
        resultlst.append(lst)    

    df=pd.DataFrame(resultlst,columns=['Word','Meaning','Example'])
    df.to_csv("./crawlingfile/test_result{}.csv".format(cnt),index=False)
    cnt+=1

