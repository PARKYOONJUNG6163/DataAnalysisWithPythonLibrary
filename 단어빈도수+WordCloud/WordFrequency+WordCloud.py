
# coding: utf-8

# In[94]:


import sys
sys.path.append("C:\\Users\\User\\Jupyter")
import pandas as pd
import csv_file as csv


# In[95]:


from collections import Counter 


# In[100]:


type = input("논문 키워드 ? ")
data_2010 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2010.csv", "UTF8", [9])
data_2011 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2011.csv", "UTF8", [9])
data_2012 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2012.csv", "UTF8", [9])
data_2013 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2013.csv", "UTF8", [9])
data_2014 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2014.csv", "UTF8", [9])
data_2015 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2015.csv", "UTF8", [9])
data_2016 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2016.csv", "UTF8", [9])
data_2017 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2017.csv", "UTF8", [9])
data_2018 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2018.csv", "UTF8", [9])
data_2019 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/" + type + "/2019.csv", "UTF8", [9])


# In[101]:


def get_frequency (data_list) :
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
    make_tf = Counter(make_list).most_common(100)
    
    return pd.DataFrame(make_tf),dict(make_tf)


# In[102]:


# 년도별로 단어와 빈도수 추출
pd_data_2010,dict_data_2010 = get_frequency(data_2010)
pd_data_2011,dict_data_2011 = get_frequency(data_2011)
pd_data_2012,dict_data_2012 = get_frequency(data_2012)
pd_data_2013,dict_data_2013 = get_frequency(data_2013)
pd_data_2014,dict_data_2014 = get_frequency(data_2014)
pd_data_2015,dict_data_2015 = get_frequency(data_2015)
pd_data_2016,dict_data_2016 = get_frequency(data_2016)
pd_data_2017,dict_data_2017 = get_frequency(data_2017)
pd_data_2018,dict_data_2018 = get_frequency(data_2018)
pd_data_2019,dict_data_2019 = get_frequency(data_2019)


# In[103]:


# 모든 년도에 속하는 단어 추출
temp = pd_data_2010[pd_data_2010[0].isin(pd_data_2011[0])]
temp = temp[temp[0].isin(pd_data_2012[0])]
temp = temp[temp[0].isin(pd_data_2013[0])]
temp = temp[temp[0].isin(pd_data_2014[0])]
temp = temp[temp[0].isin(pd_data_2015[0])]
temp = temp[temp[0].isin(pd_data_2016[0])]
temp = temp[temp[0].isin(pd_data_2017[0])]
temp = temp[temp[0].isin(pd_data_2018[0])]
temp = temp[temp[0].isin(pd_data_2019[0])]

temp.to_csv("EveryYearWords.csv", encoding = "euc-kr", index = False)
print("모든 년도에 속하는 단어 저장 성공")


# In[83]:


pd_data_2010.to_csv("2010빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2011.to_csv("2011빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2012.to_csv("2012빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2013.to_csv("2013빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2014.to_csv("2014빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2015.to_csv("2015빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2016.to_csv("2016빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2017.to_csv("2017빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2018.to_csv("2018빈도상위100.csv", encoding = "euc-kr", index = False)
pd_data_2019.to_csv("2019빈도상위100.csv", encoding = "euc-kr", index = False)
print("년도별 단어&빈도수 저장 성공")


# In[28]:


import matplotlib.pyplot as plt
from wordcloud import WordCloud


# In[29]:


font_path = "../malgun.ttf"

def make_wordCloud (tags, tags_len, filename) :
    wc = WordCloud(font_path = font_path, background_color = 'white', 
                   width = 800, height = 600, max_words = tags_len)
    cloud = wc.generate_from_frequencies(tags)
        
    figure = plt.figure(figsize = (200, 160))
    plt.imshow(cloud)
    plt.axis("off")
    figure.savefig(filename)


# In[ ]:


# wordCloud만들기
check = input("wordCloud를 만드시겠습니까? y/n ")
if(check == 'y') :
    make_wordCloud(dict_data_2010, len(dict_data_2010), './'+ type + '_data_2010.png')
    make_wordCloud(dict_data_2011, len(dict_data_2011), './'+ type + '_data_2011.png')
    make_wordCloud(dict_data_2012, len(dict_data_2012), './'+ type + '_data_2012.png')
    make_wordCloud(dict_data_2013, len(dict_data_2013), './'+ type + '_data_2013.png')
    make_wordCloud(dict_data_2014, len(dict_data_2014), './'+ type + '_data_2014.png')
    make_wordCloud(dict_data_2015, len(dict_data_2015), './'+ type + '_data_2015.png')
    make_wordCloud(dict_data_2016, len(dict_data_2016), './'+ type + '_data_2016.png')
    make_wordCloud(dict_data_2017, len(dict_data_2017), './'+ type + '_data_2017.png')
    make_wordCloud(dict_data_2018, len(dict_data_2018), './'+ type + '_data_2018.png')
    make_wordCloud(dict_data_2019, len(dict_data_2019), './'+ type + '_data_2019.png')
    print("wordCloud 저장 성공")
    
else :
    exit()

