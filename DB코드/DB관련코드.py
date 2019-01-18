
# coding: utf-8

# In[2]:

#DB 전체 목록 조회
import pymysql
conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
curs = conn.cursor()
curs.execute("show databases;")
print(curs.fetchall())

# DB 생성시 이용
query = """CREATE DATABASE s default CHARACTER SET UTF8;"""
curs.execute(query)

# DB삭제시 이용
conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
curs = conn.cursor()
query = """DROP DATABASE s; """
curs.execute(query)

# DB내용 확인시 이용
conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
curs = conn.cursor()
curs.execute("use s ;")
query = """select * from z; """
curs.execute(query)
all_rows = curs.fetchall()
for i in all_rows:
    print(i)