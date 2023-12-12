import pymysql
import pandas as pd
from db_setting import db

# '행정동_코드_김홍시_' 파일에서 area_id (행정동코드)를 읽어옵니다.
emd_areas_df = pd.read_excel('행정동_코드_김홍시_.xlsx')

# 무작위로 생성된 store_id 파일을 읽어옵니다.
store_ids_df = pd.read_csv('random_numbers_with_leading_zero.txt', header=None)

# area_id와 store_id 목록을 추출합니다.
area_ids = emd_areas_df['행정동코드'].tolist()
store_ids = store_ids_df[0].tolist()

# 필요한 경우 area_id 목록을 확장합니다.
area_ids_extended = area_ids * (len(store_ids) // len(area_ids) + 1)
area_ids_to_use = area_ids_extended[:len(store_ids)]

# 데이터베이스에 연결
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='store', charset='utf8mb4') 

try:
    with conn.cursor() as cursor:
        # 기존 데이터를 지우는 SQL문
        cursor.execute("DELETE FROM Store")

        # Store 테이블에 데이터 삽입
        for store_id, area_id in zip(store_ids, area_ids_to_use):
            name = f'Store {store_id}'
            # sql = "INSERT INTO `Store` (`store_id`, `area_id`) VALUES (%s, %s)"
            sql = "INSERT INTO `Store` (`store_id`, `area_id`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `area_id` = VALUES(`area_id`)"
            cursor.execute(sql, (store_id, area_id))

    conn.commit()
finally:
    conn.close()
    
print("데이터 삽입 완료")