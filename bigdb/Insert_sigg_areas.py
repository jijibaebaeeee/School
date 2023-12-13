import pymysql
import pandas as pd
from db_setting import db

# 엑셀 파일 읽기
df = pd.read_excel('시도단위 코드.xlsx')
df2 = pd.read_excel('행정동 기준 시군구 단위.xlsx')

# 데이터베이스 연결
conn = pymysql.connect(host=db['host'], port=db['port'],
                       user=db['Username'], passwd=db['Password'],
                       db='store', charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        
        cursor.execute("DELETE FROM sigg_areas")

        for idx, row in df.iterrows():
            
            sido_code = str(row['코드'])[:2]

            
            sigg = df2[df2['시군구코드'].astype(str).str.startswith(sido_code)]
            
            
            for _, sigg_row in sigg.iterrows():
                sql = "INSERT INTO `sigg_areas` (`id`, `sido_area_id`, `name`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (sigg_row['시군구코드'], row['코드'], sigg_row['시도_시군구']))

    # 변경 사항 저장
    conn.commit()
finally:
    conn.close()  # 데이터베이스 연결 닫기

    