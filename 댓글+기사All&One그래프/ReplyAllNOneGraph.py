
# coding: utf-8

# In[7]:


import pymysql
import pandas as pd
from pandas import DataFrame, Series

from sqlalchemy import create_engine

import matplotlib

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm 

font_location = 'C:\\Users\\User\\Jupyter\\malgun.ttf'

font_name = fm.FontProperties(fname = font_location).get_name()
matplotlib.rc('font', family = font_name)
matplotlib.rcParams.update({'font.size': 22})


# In[8]:


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


# In[9]:


matplotlib.rcParams.update({'font.size': 22})


# In[10]:


def input_value () : 
    mode = input("naver or daum ?")
    database = input("Database ? ")
    
    start_year = str(input("Start Year ? "))
    start_month = str(input("Start Month ? "))
    start_day = str(input("Start Day ? "))

    end_year = str(input("End Year ? "))
    end_month = str(input("End Month ? "))
    end_day = str(input("End Day ? "))
    
    reply_num = int(input("댓글 수 몇 개 이상 ? "))
    mode_database = mode+ '_' + database
    
    conn = db.make_connect(mode_database)
    news = db.read_by_table(mode + "_articles")
    reply = db.read_by_table(mode + "_replies")
    news_df = DataFrame(news)
    reply_df = DataFrame(reply)
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
    
    reply_df['R_Like+Bad'] = reply_df['R_Like'] + reply_df['R_Bad']
    
    group_reply_df = reply_df.groupby('Article_ID').size().to_frame('R_count')
    group_reply_df = group_reply_df[group_reply_df['R_count'] > reply_num]
    group_reply_df = group_reply_df.reset_index()
          
    news_df = news_df[news_df['Article_ID'].isin(group_reply_df['Article_ID'])]
        
    temp_reply_df = DataFrame({'Article_ID': reply_df['Article_ID'],'R_Like': reply_df['R_Like'], 'R_Bad': reply_df['R_Bad'], 'R_Like+Bad': reply_df['R_Like+Bad']})
    temp_reply_df = temp_reply_df.groupby('Article_ID').sum()
    
    temp_news_df = DataFrame({'Article_ID': news_df['Article_ID'],'Title': news_df['Title'], 'article_date' : news_df['article_date']})
    
    result_df = pd.merge(temp_news_df, group_reply_df, on = 'Article_ID')
    rank_value = int(input("상위 랭크 ? "))
    result_df = pd.merge(result_df, temp_reply_df, on = 'Article_ID')
    result_df = result_df.sort_values(by = ['R_Like+Bad'], ascending=False)
    rank_df = result_df[0:rank_value]
    print('댓글 수가 '+ str(reply_num) +' 개 이상인 기사들의 총 개수 : ' + str(len(result_df)))
    print(result_df[0:rank_value])
    
    return result_df,reply_df


# In[11]:


def make_Graph(title,filename,group_reply_df) : 
    ax = plt.figure(figsize = (30, 20))
    ax = plt.subplot(111)

    line = plt.plot(group_reply_df.index, group_reply_df.values)
    
    plt.setp(line, linewidth = 3.0, dash_joinstyle = 'round')
        
    plt.xlabel("Time")
    plt.ylabel("Count")

    plt.title(title)

    fig = plt.gcf()
    fig.autofmt_xdate()

    fig.savefig(filename + ".png")
    
    print("그래프 생성 성공")


# In[12]:


def one_make_graph (reply_df,article_id) :
    reply_df = reply_df[reply_df['Article_ID'] == article_id]
    reply_df['reply_date'] = reply_df['reply_date'].apply(lambda e: e[:16])
    group_reply_df = reply_df.groupby('reply_date').size().to_frame('R_count')
    
    # 그래프 생성하기
    graph_title = input("Graph Title ? ")
    file_name = input("File Name ? ")
    make_Graph(graph_title,file_name,group_reply_df)


# In[13]:


def all_make_graph (result_df,reply_df) :
    reply_df = reply_df[reply_df['Article_ID'].isin(result_df['Article_ID'])]
    reply_df['reply_date'] = reply_df['reply_date'].apply(lambda e: e[:16])
    group_reply_df = reply_df.groupby('reply_date').size().to_frame('R_count')
    group_reply_df['R_count']=  group_reply_df['R_count'].apply(lambda e: e/len(result_df))
    
    # 그래프 생성하기
    graph_title = input("Graph Title ? ")
    file_name = input("File Name ? ")
    make_Graph(graph_title,file_name,group_reply_df)


# In[ ]:


# 디비, 비교대상, 날짜 지정 및 추출
result_df,reply_df = input_value()
result_df.to_csv("replyLikeBad.csv", encoding = "euc-kr", index = False)
print("파일 생성 성공")
    
mode = input("all or one ?")
if (mode == 'all') :
    # 모든 기사에 대한 정보 그래프
    all_make_graph (result_df,reply_df)
elif (mode == 'one') :
    # 특정 ID에 대한 정보 그래프
    article_id = int(input("목록 중 선택할 Article_ID ?"))
    one_make_graph(reply_df,article_id)
else :
    exit()

