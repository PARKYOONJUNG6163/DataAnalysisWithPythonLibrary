
# coding: utf-8

# In[1]:


import sys
sys.path.append("C:\\Users\\User\\Jupyter")
import pandas as pd
import csv_file as csv


# In[2]:


from collections import Counter 


# In[4]:


data_2010 = csv.csv_read("C:/Users/User/Desktop/scopus논문/scopus/NPP/2010.csv", "UTF8", [9])


# In[5]:


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
    
    return dict(make_tf)


# In[6]:


dict_data_2010 = get_frequency(data_2010)


# In[7]:


import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random


# In[33]:


def grey_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 10)


# In[34]:


font_path = "../malgun.ttf"

def make_wordCloud (tags, tags_len, filename) :
    wc = WordCloud(font_path = font_path, background_color = 'white', 
                   width = 800, height = 600, max_words = tags_len)
    cloud = wc.generate_from_frequencies(tags)
    cloud = wc.recolor(color_func = grey_color_func,random_state = 3)
        
    figure = plt.figure(figsize = (200, 160))
    plt.imshow(cloud)
    plt.axis("off")
    figure.savefig(filename)


# In[35]:


make_wordCloud(dict_data_2010, len(dict_data_2010), './NPP_data_2010.png')

