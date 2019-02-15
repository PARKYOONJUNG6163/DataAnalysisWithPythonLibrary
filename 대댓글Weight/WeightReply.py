
# coding: utf-8

# In[1]:


import pymysql

import pandas as pd
from pandas import DataFrame, Series

from sqlalchemy import create_engine


# In[2]:


class MySQLConnectorWithPandas :
    
    global conn
    
    def make_connect (self, dbname) :
        print("start db connect!")
        engine = create_engine( """mysql+pymysql://root:/"""+dbname+"""?charset=utf8""", encoding = "utf8")
        self.conn = engine.connect()

    def read_by_table (self, table_name) :
        data = pd.read_sql_table(table_name, self.conn)

        return data

db = MySQLConnectorWithPandas()


# In[7]:


def input_value () : 
    mode = input("naver or daum ?")
    database = input("Database ? ")
    
    start_year = str(input("Start Year ? "))
    start_month = str(input("Start Month ? "))
    start_day = str(input("Start Day ? "))

    end_year = str(input("End Year ? "))
    end_month = str(input("End Month ? "))
    end_day = str(input("End Day ? "))

    mode_database = mode+ '_' + database
    
    conn = db.make_connect(mode_database)
    
    news = db.read_by_table(mode + "_articles")
    news_df = DataFrame(news)
    news_df.sort_values(by = ['article_date'], axis = 0, inplace = True)
    news_df = news_df[news_df.article_date != '-']
    news_df = news_df.dropna()
    
    if(mode == 'naver') : 
        news_df['article_date'] = news_df['article_date'].str.replace('최종수정 ', '')
        news_df['article_date'] = news_df['article_date'].str.replace('.', '-')

        start_date = start_year + '-' + start_month + '-' + start_day
        end_date = end_year + '-' + end_month + '-' + end_day

    elif(mode == 'daum') : 
        news_df['article_date'] = news_df['article_date'].str.replace('수정 ', '')
        news_df['article_date'] = news_df['article_date'].str.replace('입력 ', '')

        start_date = start_year + '.' + start_month + '.' + start_day
        end_date = end_year + '.' + end_month + '.' + end_day
        
    news_df = news_df[news_df.article_date > start_date]
    news_df = news_df[news_df.article_date < end_date]   
    reply = db.read_by_table(mode + "_replies")
    reply_df = DataFrame(reply)
    #기사 날짜 기준이므로 기사 날짜에 속하는 기사 ID에 속하는 댓글만 넣기
    reply_df = reply_df[reply_df['Article_ID'].isin(news_df['Article_ID'])]
    reply_df = DataFrame({'Reply_ID': reply_df['Reply_ID'], 'Writer' : reply_df['Writer']})
    
    rereply = db.read_by_table(mode + "_rereplies")
    rereply_df = DataFrame(rereply)
    rereply_df = rereply_df[rereply_df['Article_ID'].isin(news_df['Article_ID'])]
    
    group_rereply_df = rereply_df.groupby(['Article_ID','Reply_ID','ReReWriter']).size().to_frame('R_count')
    group_rereply_df = group_rereply_df.reset_index()
    temp_df = pd.merge(reply_df, group_rereply_df, on = 'Reply_ID')
    result_df= DataFrame({'Article_ID': temp_df['Article_ID'], 'Writer' : temp_df['Writer'] ,'ReReWriter' : temp_df['ReReWriter'], 'R_count' : temp_df['R_count']})
    
    return result_df


# In[8]:


result_df = input_value()
file_name = input("File Name ? ") 
result_df.to_csv(file_name + "_rereplyWeight" + ".csv", encoding = "euc-kr", index = False)
print('FINISH')

