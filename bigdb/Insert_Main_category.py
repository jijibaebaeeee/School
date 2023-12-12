import pymysql
import pandas as pd
from db_setting import db

#csv 파일 열기
#file_path = '편의점크롤링.csv'
#data = pd.read_csv(file_path, encoding='cp949')

category_map = {'a':'간편식사', 'b':'즉석조리', 'c':'과자류', 'd':'아이스크림', 'e':'식품', 'f':'음료'}


# 데이터베이스에 연결
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='store', charset='utf8mb4') 
try:
    with conn.cursor() as cursor:
        for main_id, name in category_map.items():
            sql = "INSERT INTO category (main_id, name) VALUES (%s, %s)"
            cursor.execute(sql, (main_id, name))
    
    conn.commit()
finally:
    conn.close()
    
# try:
#     with conn.cursor() as cursor:
#         # 각 고유값에 대해 삽입 쿼리 실행
#         for sub_category in unique_sub_categories:
#             sql = "INSERT INTO Sub_category (name) VALUES (%s)"
#             cursor.execute(sql, (sub_category,))

#     # 변경 사항 저장
#     conn.commit()
# finally:
#     conn.close()

# print("데이터 삽입 완료")

print("데이터 삽입 완료")