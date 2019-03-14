
# coding: utf-8

# In[1]:


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


# In[2]:


class MySQLConnectorWithPandas :
    
    global conn
    
    def make_connect (self, dbname) :
        print("start db connect!")
        engine = create_engine( """mysql+pymysql://root:1234@147.43.122.131/"""+dbname+"""?charset=utf8""", encoding = "utf8")
        self.conn = engine.connect()

    def read_by_table (self, table_name) :
        data = pd.read_sql_table(table_name, self.conn)

        return data

db = MySQLConnectorWithPandas()


# In[3]:


matplotlib.rcParams.update({'font.size': 22})


# In[4]:


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
    
    return news_df,int(start_year),int(end_year)


# In[5]:


def make_Graph(news_df,year) :
    total_count = []
    it_science = []
    economy = []
    social = []
    living_culture = []
    world = []
    politics = []
    
    need_df= DataFrame({'article_type': news_df['article_type'], 'article_date' : news_df['article_date']})
    need_df['article_date'] = need_df['article_date'].apply(lambda x : str(x[0:4]))

    for i in year :
        total = 0
        temp_df = need_df[need_df.article_date == i]
        temp_df = temp_df.groupby('article_type').size().to_frame('T_count')

        if(temp_df[temp_df.index == "IT/과학"].count().item() > 0) :
            total += temp_df.ix['IT/과학'].values[0]
            it_science.append(temp_df.ix['IT/과학'].values[0])
        else :
            it_science.append(0)

        if(temp_df[temp_df.index == "경제"].count().item() > 0) :
            total += temp_df.ix['경제'].values[0]
            economy.append(temp_df.ix['경제'].values[0])
        else :
            economy.append(0)

        if(temp_df[temp_df.index == "사회"].count().item() > 0) :
            total += temp_df.ix['사회'].values[0]
            social.append(temp_df.ix['사회'].values[0])
        else :
            social.append(0)

        if(temp_df[temp_df.index == "생활/문화"].count().item() > 0) :
            total += temp_df.ix['생활/문화'].values[0]
            living_culture.append(temp_df.ix['생활/문화'].values[0])
        else :
            living_culture.append(0)

        if(temp_df[temp_df.index == "세계"].count().item() > 0) :
            total += temp_df.ix['세계'].values[0]
            world.append(temp_df.ix['세계'].values[0])
        else :
            world.append(0)

        if(temp_df[temp_df.index == "정치"].count().item() > 0) :
            total += temp_df.ix['정치'].values[0]
            politics.append(temp_df.ix['정치'].values[0])
        else :
            politics.append(0)
            
        total_count.append(total)

    ax = plt.figure(figsize = (30, 20))
    ax = plt.subplot(111)

    plt.plot(year, it_science, label = "IT/과학")
    for i,j in zip(year, it_science):
        ax.annotate(str(j),xy=(i,j))
    plt.plot(year, economy, label = "경제")
    for i,j in zip(year, economy):
        ax.annotate(str(j),xy=(i,j))
    plt.plot(year, social, label = "사회")
    for i,j in zip(year, social):
        ax.annotate(str(j),xy=(i,j))
    plt.plot(year, living_culture, label = "생활/문화")
    for i,j in zip(year, living_culture):
        ax.annotate(str(j),xy=(i,j))
    plt.plot(year, world, label = "세계")
    for i,j in zip(year, world):
        ax.annotate(str(j),xy=(i,j))
    plt.plot(year, politics, label = "정치")
    for i,j in zip(year, politics):
        ax.annotate(str(j),xy=(i,j))
    plt.plot(year, total_count, label = "total count")
    for i,j in zip(year, total_count):
        ax.annotate(str(j),xy=(i,j))
        
    plt.xlabel('Year')
    plt.ylabel('Count')

    plt.title('Number for News Type')

    plt.legend()
    
    filename = input("Count/Year 그래프를 저장할 파일의 이름 ?")
    
    fig = plt.gcf()
    fig.autofmt_xdate()
    
    fig.savefig(filename + ".png")

    make_per_Graph(year,total_count,it_science,economy,social,living_culture,world,politics)


# In[6]:


def make_per_Graph(year,total_count,it_science,economy,social,living_culture,world,politics) :
    p_it_science = [round((it_science[i]/total_count[i])* 100,0) for i in range(len(total_count))]
    p_economy = [round((economy[i]/total_count[i])* 100,0) for i in range(len(total_count))]
    p_social = [round((social[i]/total_count[i])* 100,0) for i in range(len(total_count))]
    p_living_culture = [round((living_culture[i]/total_count[i])* 100,0) for i in range(len(total_count))]
    p_world = [round((world[i]/total_count[i])* 100,0) for i in range(len(total_count))]
    p_politics = [round((politics[i]/total_count[i])* 100,0) for i in range(len(total_count))]
        
    
    ax = plt.figure(figsize = (30, 20))
    ax = plt.subplot(111)

    plt.plot(year, p_it_science, label = "IT/과학")
    for i,j in zip(year, p_it_science):
        ax.annotate(str(j)+"%",xy=(i,j))
    plt.plot(year, p_economy, label = "경제")
    for i,j in zip(year, p_economy):
        ax.annotate(str(j)+"%",xy=(i,j))
    plt.plot(year, p_social, label = "사회")
    for i,j in zip(year, p_social):
        ax.annotate(str(j)+"%",xy=(i,j))
    plt.plot(year, p_living_culture, label = "생활/문화")
    for i,j in zip(year, p_living_culture):
        ax.annotate(str(j)+"%",xy=(i,j))
    plt.plot(year, p_world, label = "세계")
    for i,j in zip(year, p_world):
        ax.annotate(str(j)+"%",xy=(i,j))
    plt.plot(year, p_politics, label = "정치")
    for i,j in zip(year, p_politics):
        ax.annotate(str(j)+"%",xy=(i,j))
        
    plt.xlabel('Year')
    plt.ylabel('Percent')

    plt.title('Percent for News Type')

    plt.legend()
    
    filename = input("Percent/Year 그래프를 저장할 파일의 이름 ?")
    
    fig = plt.gcf()
    fig.autofmt_xdate()
    
    fig.savefig(filename + ".png")


# In[7]:


def make_file(news_df,file_num) :
    count = 0
    while count < file_num :
        article_type = int(input("파일로 저장할 분야? 1.IT/과학 2.경제 3.사회 4.생활/문화 5.세계 6.정치 "))
        name = input("저장할 파일의 이름 ?")
        if article_type == 1 : # IT/과학 파일로 
            temp_df = news_df[news_df.article_type == 'IT/과학']
            temp_df.to_csv(name + ".csv", encoding = "euc-kr", index = False)
        elif article_type == 2 :
            temp_df = news_df[news_df.article_type == '경제']
            temp_df.to_csv(name + ".csv", encoding = "euc-kr", index = False)
        elif article_type == 3 :
            temp_df = news_df[news_df.article_type == '사회']
            temp_df.to_csv(name + ".csv", encoding = "euc-kr", index = False)
        elif article_type == 4 :
            temp_df = news_df[news_df.article_type == '생활/문화']
            temp_df.to_csv(name + ".csv", encoding = "euc-kr", index = False)
        elif article_type == 5 :
            temp_df = news_df[news_df.article_type == '세계']
            temp_df.to_csv(name + ".csv", encoding = "euc-kr", index = False)
        elif article_type == 6 :
            temp_df = news_df[news_df.article_type == '정치']
            temp_df.to_csv(name + ".csv", encoding = "euc-kr", index = False)
        print("파일 생성 완료")
        count += 1


# In[ ]:


news_df,start_year,end_year = input_value()

year = []
while start_year <= end_year :
    year.append(str(start_year))
    start_year += 1

make_Graph(news_df,year)

select_type = []
saved_file =  input("cvs 파일로 저장하시겠습니까 ? y/n ")
if (saved_file == 'y') :
    file_num = int(input("몇 개를 파일로 저장하시겠습니까 ?"))
    make_file(news_df, file_num)   
    print("파일 저장 후 Finish!")
else :
    print("파일 저장 안하고 Finish!")
    exit()

