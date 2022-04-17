import pandas as pd
from glob import glob
import re


#어휘부분 깨진문자 제거
def remove_garbledword(origin_filename,new_filename):
    data=pd.read_csv(origin_filename)
    wordlst=data['어휘'].values.tolist()
    print(type(wordlst[0]))
    print(len(wordlst))

    for word in wordlst:
        if '?' in word:
            print(word)
            wordlst.remove(word)
    print(len(wordlst))

    df = pd.DataFrame(wordlst, columns = ['어휘'])
    df.to_csv(new_filename,index=False)


    
for i in range(1,7):
    remove_garbledword('word_only{}.csv'.format(i),'new_word_only{}.csv'.format(i))