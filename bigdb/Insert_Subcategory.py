# import pymysql
# from db_setting import db
# from CU_Crawling_selenium_each import SUBCATEGORY
# # 데이터베이스 연결 설정
# connection = pymysql.connect(host = db['host'], 
#                              user = db['Username'], 
#                              password = db['Password'], 
#                              db = 'Convenience_store', 
#                              charset='utf8', 
#                              cursorclass=pymysql.cursors.DictCursor)

# # try:
# #     with connection.cursor() as cursor:
# #         # SUBCATEGORY의 데이터 삽입
# #         sub_id_counter = 1
# #         for main_cat, sub_categories in SUBCATEGORY.items():
# #             for sub_cat in sub_categories:
# #                 sql = "INSERT INTO `Sub_category` (`sub_id`, `name`) VALUES (%s, %s)"
# #                 cursor.execute(sql, (sub_id_counter, sub_cat))
# #                 sub_id_counter += 1

# #         # 변경사항 커밋
# #         connection.commit()

# # finally:
# #     connection.close()
# try:
#     with connection.cursor() as cursor:
#         sub_id_counter = 1
#         for main_cat, sub_categories in SUBCATEGORY.items():
#             for sub_cat in sub_categories:
#                 # 중복 확인
#                 sql = "SELECT * FROM `Sub_category` WHERE `name` = %s"
#                 cursor.execute(sql, (sub_cat,))
#                 result = cursor.fetchone()
                    
#                 # 중복이 없는 경우에만 삽입
#                 if not result:
#                     sql = "INSERT INTO `Sub_category` (`sub_id`, `name`) VALUES (%s, %s)"
#                     cursor.execute(sql, (sub_id_counter, sub_cat))
#                     sub_id_counter += 1

#         # 변경사항 커밋
#         connection.commit()

# finally:
#     connection.close()
# CSV 파일을 불러옴
import pymysql
import pandas as pd
from db_setting import db

file_path = '편의점크롤링.csv'
data = pd.read_csv(file_path, encoding='cp949')

# '서브분류' 열에서 고유한 값 추출
unique_sub_categories = data['서브분류'].unique()

# 데이터베이스에 연결
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='store', charset='utf8mb4') 

try:
    with conn.cursor() as cursor:
        # 각 고유값에 대해 삽입 쿼리 실행
        for sub_category in unique_sub_categories:
            sql = "INSERT INTO Sub_category (name) VALUES (%s)"
            cursor.execute(sql, (sub_category,))

    # 변경 사항 저장
    conn.commit()
finally:
    conn.close()

print("데이터 삽입 완료")