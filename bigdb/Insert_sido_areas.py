import pymysql
import pandas as pd
from db_setting import db

# # 엑셀 파일 읽기
df = pd.read_excel('시도단위 코드.xlsx')

# 데이터베이스 연결
conn = pymysql.connect(host=db['host'], port=db['port'],
                       user=db['Username'], passwd=db['Password'],
                       db='store', charset='utf8mb4')  # 'store'는 실제 데이터베이스 이름으로 변경해주세요.

try:
    with conn.cursor() as cursor:
        # 기존 데이터를 지우는 SQL문 (테이블을 새로운 데이터로 재설정하려는 경우)
        cursor.execute("DELETE FROM sido_areas")  # 기존 데이터를 유지하려면 이 줄을 제거하세요.
        
        # DataFrame의 각 행에 대해 INSERT SQL문 실행
        for idx, row in df.iterrows():
            sql = "INSERT INTO `sido_areas` (`id`, `name`) VALUES (%s, %s)"
            cursor.execute(sql, (row['코드'], row['시도_이름']))

    # 변경 사항 저장
    conn.commit()
finally:
    conn.close()  # 데이터베이스 연결 닫기