
# coding: utf-8

# In[10]:


import pymysql
import pandas as pd

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


# In[11]:


class MySQLConnectorWithPandas :
    
    global conn
    
    def make_connect (self, dbname) :
        print("start db connect!")
        engine = create_engine( """mysql+pymysql://root:1234@147.43.122.34/"""+dbname+"""?charset=utf8""", encoding = "utf8")
        self.conn = engine.connect()

    def make_connect_local (self, dbname) :
        print("start db connect!")
        engine = create_engine( """mysql+pymysql://root:1234@localhost/"""+dbname+"""?charset=utf8""", encoding = "utf8")
        self.conn = engine.connect()

    def read_by_query (self, query) :
        data = pd.read_sql_query(query, self.conn)

        return data 

    def read_by_table (self, table_name) :
        data = pd.read_sql_table(table_name, self.conn)

        return data

db = MySQLConnectorWithPandas()


# In[12]:


matplotlib.rcParams.update({'font.size': 22})


# In[13]:


def input_value () : 
    mode1 = input("첫 번째 비교 대상 naver or daum ?")
    mode2= input("두 번째 비교 대상 naver or daum ?")
    database1 = input("첫번째 Database ? ")
    database2 = input("두번째 Database ? ")
    
    start_year = str(input("Start Year ? "))
    start_month = str(input("Start Month ? "))
    start_day = str(input("Start Day ? "))

    end_year = str(input("End Year ? "))
    end_month = str(input("End Month ? "))
    end_day = str(input("End Day ? "))

    print()
    
    mode1_database = mode1+ '_' + database1
    mode2_database = mode2+ '_' + database2
    
    conn = db.make_connect(mode1_database)
    first_news = db.read_by_table(mode1 + "_articles")
    f_reply = db.read_by_table(mode1 + "_replies")
    first_df = DataFrame(first_news)
    f_reply_df = DataFrame(f_reply)
    first_df.sort_values(by = ['article_date'], axis = 0, inplace = True)
    first_df = first_df[first_df.article_date != '-']
    first_df = first_df.dropna()
    
    conn = db.make_connect(mode2_database)
    second_news = db.read_by_table(mode2 + "_articles")
    s_reply = db.read_by_table(mode2 + "_replies")
    s_reply_df = DataFrame(s_reply)
    second_df = DataFrame(second_news)
    second_df.sort_values(by = ['article_date'], axis = 0, inplace = True)
    second_df = second_df[second_df.article_date != '-']
    second_df = second_df.dropna()
        
    if(mode1 == 'naver') : 
        first_df['article_date'] = first_df['article_date'].str.replace('최종수정 ', '')
        first_df['article_date'] = first_df['article_date'].str.replace('.', '-')
        
        start_date1 = start_year + '-' + start_month + '-' + start_day
        end_date1 = end_year + '-' + end_month + '-' + end_day
    
    elif(mode1 == 'daum') : 
        first_df['article_date'] = first_df['article_date'].str.replace('수정 ', '')
        first_df['article_date'] = first_df['article_date'].str.replace('입력 ', '')
        
        start_date1 = start_year + '.' + start_month + '.' + start_day
        end_date1 = end_year + '.' + end_month + '.' + end_day
        
    if(mode2 == 'naver') : 
        second_df['article_date'] = second_df['article_date'].str.replace('최종수정 ', '')
        second_df['article_date'] = second_df['article_date'].str.replace('.', '-')
        
        start_date2 = start_year + '-' + start_month + '-' + start_day
        end_date2 = end_year + '-' + end_month + '-' + end_day

    elif(mode2 == 'daum') : 
        second_df['article_date'] = second_df['article_date'].str.replace('수정 ', '')
        second_df['article_date'] = second_df['article_date'].str.replace('입력 ', '')
        
        start_date2 = start_year + '.' + start_month + '.' + start_day
        end_date2 = end_year + '.' + end_month + '.' + end_day
    
    first_df = first_df[first_df.article_date > start_date1]
    first_df = first_df[first_df.article_date < end_date1]
    second_df = second_df[second_df.article_date > start_date2]
    second_df = second_df[second_df.article_date < end_date2]
        
    
    temp1 = first_df['Title']
    temp2 = second_df['Title']
    
    same1 = first_df[temp1.isin(temp2)]
    same2 = second_df[temp2.isin(temp1)]
    
#     same1 = same1.drop_duplicates(['Title'])
#     same2 = same2.drop_duplicates(['Title'])
    
    print("총 기사의 개수 : %d" % (len(temp1)+len(temp2)))

    print("같은 기사의 개수 : %d" % len(same1))   
    print("다른 기사의 개수 : %d" % (len(temp1)+len(temp2)-len(same1)))
    
#     양을 줄이기 위해 필요한 부분만 다시 데이터프레임으로 만듬
    f_temp_df = DataFrame({'Article_ID': same1['Article_ID'],'Title': same1['Title'], 'article_date' : same1['article_date']})
    s_temp_df = DataFrame({'Article_ID': same2['Article_ID'],'Title': same2['Title'], 'article_date' : same2['article_date']})
    
#     댓글과 기사 합치기
    f_reply_data = pd.merge(f_reply_df, f_temp_df, on = 'Article_ID')
    s_reply_data = pd.merge(s_reply_df, s_temp_df, on = 'Article_ID')
    
    make_reply_file(f_reply_data,s_reply_data)
    
    return  mode1,mode2,f_reply_data,s_reply_data,len(same1)


# In[14]:


def make_rank_Data(mode1,mode2,f_reply_data,s_reply_data) : 
    rank_value = int(input("상위 랭크 ? "))
    
    f_reply_data['Writer'] = f_reply_data['Writer'].str.replace(' ', '')
    f_reply_data = f_reply_data.groupby(['Writer']).size()
    f_result = f_reply_data.sort_values(ascending=False)
    
    s_reply_data['Writer'] = s_reply_data['Writer'].str.replace(' ', '')
    s_reply_data= s_reply_data.groupby(['Writer']).size()
    s_result = s_reply_data.sort_values(ascending=False)
    
    print("---" + mode1 + "데이터---")    
    print(f_result[0:rank_value])
    
    print()
    
    print("---" + mode2 + "데이터---")    
    print(s_result[0:rank_value])
    
    return f_result[0:rank_value],s_result[0:rank_value]


# In[15]:


def make_rank_Graph(title,filename,mode,result) : 
    ax = plt.figure(figsize = (30, 20))
    ax = plt.subplot(111)
    
    line = plt.plot(result.index, result.values)
    
    plt.setp(line, linewidth = 3.0, dash_joinstyle = 'round')
    
    for i,j in zip(result.index, result.values):
        ax.annotate(str(j),xy=(i,j))
        
    plt.xlabel("Writer")
    plt.ylabel("count")

    plt.title(title)

    fig = plt.gcf()
    fig.autofmt_xdate()
    
    fig.savefig(filename + ".png")
    
    print("그래프 생성 성공")


# In[16]:


def make_reply_file(f_reply_data,s_reply_data) :
    f_reply_data.to_csv("첫번째_비교대상_같은기사&댓글" + ".csv", encoding = "euc-kr", index = False)
    print("파일 생성 성공")

    s_reply_data.to_csv("두번째_비교대상_같은기사&댓글" + ".csv", encoding = "euc-kr", index = False)
    print("파일 생성 성공")
    
    print()    


# In[17]:


def make_rank_file(f_reply_data,f_result,s_reply_data,s_result) :
    f_old = pd.DataFrame()
    f_reply_data['Writer'] = f_reply_data['Writer'].str.replace(' ', '')
    
    for i in f_result.index :
        f_new = f_reply_data[f_reply_data["Writer"] == i]
        f_old = pd.concat([f_old,f_new])
        
    f_temp_df = DataFrame({'Writer': f_old['Writer'],'Reply': f_old['Reply'],'Title': f_old['Title'],'R_Like': f_old['R_Like'], 'R_Bad': f_old['R_Bad'],'article_date': f_old['article_date']})
    f_temp_df.to_csv("첫번째_비교대상_순위&댓글" + ".csv", encoding = "euc-kr", index = False)
    print("파일 생성 성공")
    
    s_old = pd.DataFrame()
    s_reply_data['Writer'] = s_reply_data['Writer'].str.replace(' ', '')
    
    for i in s_result.index :
        s_new = s_reply_data[s_reply_data["Writer"] == i]
        s_old = pd.concat([s_old,s_new])
        
    s_temp_df = DataFrame({'Writer': s_old['Writer'],'Reply': s_old['Reply'],'Title': s_old['Title'],'R_Like': s_old['R_Like'], 'R_Bad': s_old['R_Bad'],'article_date': s_old['article_date']})
    s_temp_df.to_csv("두번째_비교대상_순위&댓글" + ".csv", encoding = "euc-kr", index = False)
    print("파일 생성 성공")
    
    print()


# In[18]:


# 디비, 비교대상, 날짜 지정 및 추출
mode1,mode2,f_reply_data,s_reply_data,count = input_value ()

if(count != 0) : 
    # 비교 대상 두 개의 각각의 댓글과 기사를 합쳐서 파일로 저장
    make_reply_file(f_reply_data,s_reply_data)
    
    # 비교 대상 두 개의 각각의 순위만큼의 결과 추출
    f_result,s_result = make_rank_Data(mode1,mode2,f_reply_data,s_reply_data)
    
    # 비교 대상 두 개의 각각의 그래프 생성
    graph_title = input("Graph Title ? ")
    file_name = input("File Name ? ")
    make_rank_Graph(graph_title,file_name,mode1,f_result)
    
    graph_title = input("Graph Title ? ")
    file_name = input("File Name ? ")
    make_rank_Graph(graph_title,file_name,mode2,s_result)
    
    store = input("상위 랭크 댓글들을 저장하시겠습니까? y/n")
    if(store == "y") :
        # 순위만큼의 작성자들의 댓글을 파일로 저장
        make_rank_file(f_reply_data,f_result,s_reply_data,s_result)
    else :
        exit()
        
else :
        print("같은 기사가 없으므로 종료합니다.")
        exit()

