import pymysql
import pandas as pd
from db_setting import db

# 엑셀 파일 읽기
df = pd.read_csv('편의점크롤링_행사.csv', encoding='cp949')

# NaN 값이 있는지 확인하고, 있다면 None으로 대체합니다.
df = df.where(pd.notnull(df), None)

# category_map 정의
category_map = {'a': '간편식사', 'b': '즉석조리', 'c': '과자류', 'd': '아이스크림', 'e': '식품', 'f': '음료'}

# 데이터베이스 연결
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='store', charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        for index, row in df.iterrows():
            # main_id 매핑
            main_id = [key for key, value in category_map.items() if value == row['메인분류']][0] if row['메인분류'] else None

            # sub_id 조회
            if row['서브분류']:
                cursor.execute("SELECT sub_id FROM Sub_category WHERE main_id = %s AND name = %s", (main_id, row['서브분류']))
                sub_result = cursor.fetchone()
                sub_id = sub_result[0] if sub_result else None
            else:
                sub_id = None

            # event_id 조회 (이벤트 이름이 엑셀 데이터에 있는 경우)
            event_name = row['행사']  # 이벤트 이름 열의 이름을 '행사'로 가정
            if event_name and event_name != 'NULL':  # None 이거나 'NULL'이 아닌 경우에만 조회
                cursor.execute("SELECT event_id FROM Event WHERE event_name = %s", (event_name,))
                event_result = cursor.fetchone()
                event_id = event_result[0] if event_result else None
            else:
                event_id = None

            # INSERT 쿼리 실행
            sql = "INSERT INTO Product (product_id, main_id, sub_id, name, price, event_id) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (row['ID'], main_id, sub_id, row['상품명'], row['가격'], event_id))

    # 변경 사항 저장
    conn.commit()
finally:
    conn.close()