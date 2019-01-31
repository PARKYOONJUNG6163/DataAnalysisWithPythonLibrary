
# coding: utf-8

# In[4]:


import pymysql
import pandas as pd

from pandas import DataFrame, Series
from sqlalchemy import create_engine

import datetime


# In[5]:


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


# In[8]:


choice = input("naver or daum ? ")
database = input("Database ? ")
term_num = int(input("몇 개의 기간 ?"))
count = 0
date_list = []
day_1 = datetime.timedelta(days=1)

while term_num > count :
    start_date = str(input("시작 기한 ? "))
    end_date = str(input("끝나는 기한 ? "))
    date_list.append([start_date,end_date])
    count += 1


# In[10]:


dbname = choice + '_' + database
conn = db.make_connect(dbname)

if(choice == 'naver') :
    news = db.read_by_table("naver_articles")    
elif(choice == 'daum') :
    news = db.read_by_table("daum_articles") 

news_df = DataFrame(news)
news_df.sort_values(by = ['article_date'], axis = 0, inplace = True)
news_df = news_df[news_df.article_date != '-']
news_df = news_df.dropna()

for i in date_list :
    temp_df = news_df[news_df.article_date.between(i[0], str(pd.to_datetime(i[1]) + day_1))]
    temp_df.to_csv(dbname+"_"+i[0]+"_"+i[1]+".csv", encoding = "euc-kr", index = False)
    print(i[0]+"~"+i[1]+" 파일 생성 성공!")

