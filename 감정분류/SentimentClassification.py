
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

    def make_connect_local (self, dbname) :
        print("start db connect!")
        engine = create_engine( """mysql+pymysql://root:/"""+dbname+"""?charset=utf8""", encoding = "utf8")
        self.conn = engine.connect()

    def read_by_query (self, query) :
        data = pd.read_sql_query(query, self.conn)

        return data 

    def read_by_table (self, table_name) :
        data = pd.read_sql_table(table_name, self.conn)

        return data

db = MySQLConnectorWithPandas()


# In[3]:


def input_value () : 
    mode = input("naver or daum ?")
    database = input("Database ? ")
    
    mode_database = mode+ '_' + database
    
    conn = db.make_connect(mode_database)
    news = db.read_by_table(mode + "_articles")
    news_df = DataFrame(news)
    
    # 무관심인건 제거
    news_df = news_df[news_df.article_sentiment != 2]
    news_df = news_df.dropna()

    print('평균 긍정 지수:=',format(news_df['article_per'].mean(), '.2f'))
    print('긍정/부정/중립 총 합:=',news_df['article_sentiment'].sum())
    print('전체 개수:=',len(news_df))
    
    return news_df


# In[4]:


news_df = input_value ()

is_saved = input('파일로 저장하시겠습니까? y/n')
if is_saved == 'y' :
    file_name = input('파일 이름 ? ')
    news_df.to_csv(file_name + ".csv", encoding = "euc-kr", index = False)
    print('파일 저장 성공!')
else :
    print('프로그램 종료')

