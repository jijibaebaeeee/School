# CSV 파일을 불러옴
import pymysql
import pandas as pd
from db_setting import db

file_path = '편의점크롤링.csv'
data = pd.read_csv(file_path, encoding='cp949')

# '서브분류' 열에서 고유한 값 추출
Main_category = {'간편식사': 'a', '즉석조리': 'b', '과자류': 'c', '아이스크림': 'd', '식품': 'e', '음료': 'f'}
unique_main_categories_name = data['메인분류'].unique()


# 데이터베이스에 연결
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='Convience_store', charset='utf8mb4')  # 데이터베이스 이름을 지정해주세요

try:
    with conn.cursor() as cursor:
        # 각 고유값에 대해 삽입 쿼리 실행
        for main_category in unique_sub_categories:
            sql = "INSERT INTO Sub_category (name) VALUES (%s)"
            cursor.execute(sql, (sub_category,))

    # 변경 사항 저장
    conn.commit()
finally:
    conn.close()

print("데이터 삽입 완료")