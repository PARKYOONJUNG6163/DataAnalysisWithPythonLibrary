
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import DataFrame, Series
from sqlalchemy import create_engine


# In[2]:


def getDB(news_type, dbname, option):
    database = news_type + '_' + dbname
    engine = create_engine( """mysql+pymysql://root:@/"""+database+"""?charset=utf8""", encoding = "utf8")
    conn = engine.connect()
    
    if option == 1 :
        data = pd.read_sql_table(news_type +'_articles', conn)
    elif option == 2 :
        data = pd.read_sql_table(news_type +'_replies', conn)
    else :
        data = pd.read_sql_table(news_type +'_rereplies', conn)
    
    return DataFrame(data)


# In[3]:


def article_group_sentiment(data_df, sentiment_num) :
    if sentiment_num == 1 : # 긍정
        group_data_df = data_df[data_df.article_sentiment == 1]
    elif sentiment_num == 2 : # 부정
        group_data_df = data_df[data_df.article_sentiment == -1]
    elif sentiment_num == 3 : # 중립
        group_data_df = data_df[data_df.article_sentiment == 0]
    else : # 무관심
        group_data_df = data_df[data_df.article_sentiment == 2]
    #파일로 저장
    make_file(group_data_df) 


# In[4]:


def reply_group_sentiment(data_df, sentiment_num) :
    if sentiment_num == 1 : # 긍정
        group_data_df = data_df[data_df.R_Sentiment == 1]
    elif sentiment_num == 2 : # 부정
        group_data_df = data_df[data_df.R_Sentiment == -1]
    elif sentiment_num == 3 : # 중립
        group_data_df = data_df[data_df.R_Sentiment == 0]
    else : # 무관심
        group_data_df = data_df[data_df.R_Sentiment == 2]
    #파일로 저장
    make_file(group_data_df) 


# In[5]:


def make_file(group_data_df) :
    save = input('파일로 저장하시겠습니까? y/n ')
    if save == 'y' :
        try :
            file_name = input('파일 이름을 입력해주세요. ')
            group_data_df.to_csv(file_name+".csv", encoding = "euc-kr", index = False)
            print('파일 저장 성공')
        except : 
            print('파일 저장 실패')
    else :
        print('FINISH')


# In[6]:


def input_value() :
    news_type = input('naver or daum ?')
    option = int(input('1. 기사 / 2. 댓글 / 3. 대댓글 ?'))
    dbname = input('database 이름 ?')
    data_df = getDB(news_type, dbname, option)
    sentiment_num = int(input('1. 긍정 / 2. 부정 / 3. 중립 / 4. 무관심 ?'))
    
    if option == 1 :
        article_group_sentiment(data_df, sentiment_num)
    else :
        reply_group_sentiment(data_df, sentiment_num)


# In[8]:


input_value()

