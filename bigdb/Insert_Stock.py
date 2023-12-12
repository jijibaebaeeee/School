import pymysql
import random
from db_setting import db
# 데이터베이스 연결 설정 (DB 정보를 채워주세요)
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='store', charset='utf8mb4') 
# 커서 생성
cursor = conn.cursor()

try:
    # Store 테이블의 모든 store_id 가져오기
    cursor.execute("SELECT `store_id` FROM `Store`")
    store_ids = cursor.fetchall()

    # Product 테이블에서 product_id, main_id, sub_id 가져오기 (LIMIT을 사용하여 원하는 수만큼 가져올 수 있습니다)
    cursor.execute("SELECT `product_id`, `main_id`, `sub_id` FROM `Product` LIMIT 200")
    products = cursor.fetchall()

    # INSERT 쿼리 실행 (각 store_id에 대해)
    for store_id in store_ids:
        for product in products:
            # count 값을 0부터 10 사이의 무작위 정수로 설정
            count = random.randint(0, 10)
            # store_id, product_id, main_id, sub_id, count를 이용하여 INSERT 쿼리 실행
            insert_query = "INSERT INTO `Stock` (`store_id`, `product_id`, `main_id`, `sub_id`, `count`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (store_id[0], product[0], product[1], product[2], count))
    
    # 변경사항 저장
    conn.commit()

    print("데이터 삽입 완료")

except Exception as e:
    print(f"오류 발생: {str(e)}")
finally:
    # 연결 종료
    cursor.close()
    conn.close()