import pymysql
from db_setting import db
import pandas as pd
# from CU_Crawling_selenium_each import MAINCATEGORY, SUBCATEGORY

#csv 파일 열기
file_path = '편의점크롤링.csv'
data = pd.read_csv(file_path, encoding='cp949')

connection = pymysql.connect(host = db['host'], user = db['Username'], password = db['Password'], db = 'Convenience_store', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # MAINCATEGORY의 데이터 삽입
        for main_id, main_name in MAINCATEGORY.items():
            sql = "INSERT INTO `category` (`main_id`, `name`) VALUES (%s, %s)"
            cursor.execute(sql, (main_id, main_name))
            # SUBCATEGORY의 데이터 삽입
            for sub_id, sub_name in enumerate(SUBCATEGORY[main_id], 1):
                sql = "INSERT INTO `Sub_category` (`sub_id`, `name`) VALUES (%s, %s)"
                cursor.execute(sql, (sub_id, sub_name))

  # 변경사항 커밋
    connection.commit()

finally:
    connection.close()




# try:
#     with conn.corsor() as curs:
#         sql = "INSERT INTO category VALUES"
#         curs.execute() # 실행할 sql문 넣기
#         rs = curs.fetchall() # sql문 실행해서 데이터 가져오기

#         for row in rs:
#             for data in row:
#                 print(data, end=' ')
#             print()

# finally:
#     conn.clsoe()