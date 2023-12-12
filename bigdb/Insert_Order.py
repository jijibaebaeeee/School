import pymysql
import random
from db_setting import db

# 데이터베이스 연결
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='store', charset='utf8mb4') 

try:
    with conn.cursor() as cursor:
        for _ in range(700):
            

            # Store 테이블에서 임의의 store_id 가져오기
            cursor.execute("SELECT store_id FROM Store ORDER BY RAND() LIMIT 1")
            store_id_value = cursor.fetchone()[0]

            # Product 테이블에서 임의의 product_id 가져오기
            cursor.execute("SELECT product_id FROM Product ORDER BY RAND() LIMIT 1")
            product_id_value = cursor.fetchone()[0]

            # 1부터 10 사이의 임의의 숫자 생성
            cnt_value = random.randint(1, 10)

            # Order 테이블에 데이터 삽입
            sql = "INSERT INTO `ord` (`store_id`, `product_id`, `cnt`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (store_id_value, product_id_value, cnt_value))

        # 변경 사항 저장
        conn.commit()
finally:
    conn.close()