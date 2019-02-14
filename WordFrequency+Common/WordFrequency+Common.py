
# coding: utf-8

# In[1]:


import sys
sys.path.append("C:\\Users\\User\\Jupyter")
import pandas as pd
from pandas import DataFrame, Series
import csv


# In[2]:


from collections import Counter 


# In[3]:


def csv_read(filename, encode, num_list) : 
    file_list =  list()
    file = open(filename, "r", encoding = encode)
    file_read = csv.reader(file)
    
    for line in file_read : 
        for num in num_list:
            file_list.append(line[num])
            
    file.close()
    return file_list


# In[4]:


def get_frequency (data_list,rank) :
    make_list = list()
    check = 0
    
    for data in data_list :
        if(check < 1) :
            check = check + 1
        elif (data == ''):
            continue
        else :
            temp = data.split(';')
            for i in temp :
                i = i.strip()
                make_list.append(i) 
                
    # 상위 100위 까지만 추출
    make_tf = Counter(make_list).most_common(int(rank))
    
    return pd.DataFrame(make_tf)


# In[5]:


def input_value() :
    file_num = int(input("csv 파일 몇개? "))
    file_list = []
    count = 0
    while file_num > count :
        file_name = input("파일명을 입력하세요 ")
        file_list.append(file_name)
        count += 1
    cell_num = int(input("몇 번째 셀? ex) A이면 0을, C면 2를 ... "))
    rank = input('상위 몇 개?')
    return file_list,cell_num,file_num,rank


# In[6]:


def make_merge_df(file_list,cell_num,file_num,rank) :
    df_list = []
    for file in file_list :
        data = csv_read("./" + file , "cp949", [cell_num])
        pd_data = get_frequency(data,rank)
        df_list.append(pd_data)
    i = 1
    merge_df = df_list[0]
    while i < file_num :
        merge_df = pd.concat([merge_df, df_list[i]], axis=1)
        i += 1
        
    #파일로 저장  
    try :
        file_name = input("생성할 년도별로 합친 파일 이름? ")
        merge_df.to_csv(file_name+".csv", encoding = "euc-kr", index = False)
        print('파일 저장 성공')
    except : 
        print('파일 저장 실패')
        
    return df_list


# In[7]:


def common_word(df_list,file_num) :
    # 모든 년도에 속하는 단어 추출
    i = 1
    temp = df_list[0]
    while i < file_num :
        temp = temp[temp[0].isin(df_list[i][0])]
        i += 1
    
    #파일로 저장  
    try :
        file_name = input("생성할 공통 단어 모아둔 파일 이름? ")
        temp[0].to_csv(file_name+".csv", encoding = "euc-kr", index = False)
        print('파일 저장 성공')
    except : 
        print('파일 저장 실패')


# In[8]:


file_list,cell_num,file_num,rank = input_value()
df_list = make_merge_df(file_list,cell_num,file_num,rank)
common_word(df_list,file_num)

