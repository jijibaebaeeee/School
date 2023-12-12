import pymysql
import pandas as pd
from db_setting import db

#csv 파일 열기
#file_path = '편의점크롤링.csv'
#data = pd.read_csv(file_path, encoding='cp949')

# 데이터베이스에 연결
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='store', charset='utf8mb4') 

event_name1 = '1plus1'
event_name2 = '2plus1'
event_name3 = '30_percent_discount'
evnet_name4 = '50_percent_discount'


try:
    with conn.cursor() as cursor:
            sql = "INSERT INTO Event (event_name, card_name) VALUES (%s, %s)"
            cursor.execute(sql, (event_name1, ))
    
    conn.commit()
finally:
    conn.close()