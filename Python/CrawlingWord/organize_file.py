import pandas as pd
from glob import glob
import re


#어휘부분 불필요한 문자 제거
def write(before):
    p = re.compile("[^0-9]")
    if before is not None:  
        before = before.replace("-","")
        before = before.replace("ㆍ","")
        before = before.replace("^","")
        after = before.replace(":","")
        after = "".join(p.findall(after))
        return after


files = glob('전체 내려받기_우리말샘_xls_20220302/*.xls')

dataframe = pd.DataFrame()
for file in files:
    data = pd.read_excel(file,sheet_name='Sheet0')
    dataframe = dataframe.append(data)
    
new_data=dataframe[['어휘','뜻풀이','용례']]

new_data_1=new_data.iloc[:200000,:]
new_data_2=new_data.iloc[200000:400000,:]
new_data_3=new_data.iloc[400000:600000,:]
new_data_4=new_data.iloc[600000:800000,:]
new_data_5=new_data.iloc[800000:1000000,:]
new_data_6=new_data.iloc[1000000:,:]

new_data_1['어휘'] = new_data_1['어휘'].apply(write)
new_data_2['어휘'] = new_data_2['어휘'].apply(write)
new_data_3['어휘'] = new_data_3['어휘'].apply(write)
new_data_4['어휘'] = new_data_4['어휘'].apply(write)
new_data_5['어휘'] = new_data_5['어휘'].apply(write)
new_data_6['어휘'] = new_data_6['어휘'].apply(write)

new_data_1=new_data_1.drop_duplicates(['어휘'],keep='first')
new_data_2=new_data_2.drop_duplicates(['어휘'],keep='first')
new_data_3=new_data_3.drop_duplicates(['어휘'],keep='first')
new_data_4=new_data_4.drop_duplicates(['어휘'],keep='first')
new_data_5=new_data_5.drop_duplicates(['어휘'],keep='first')
new_data_6=new_data_6.drop_duplicates(['어휘'],keep='first')
    
for i in range(1,7):
    new_data_1.to_csv('new_data_{}.csv'.format(i),index=False)    