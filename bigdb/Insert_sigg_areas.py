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
        # 기존 데이터를 지우는 SQL문 (테이블을 새로운 데이터로 재설정하려는 경우)
        cursor.execute("DELETE FROM sigg_areas")

        # 시도 코드의 앞 두 자리를 기반으로 시군구 코드를 매핑하고 INSERT 문 생성
        for idx, row in df.iterrows():
            # 시도 코드의 앞 두 자리 추출
            sido_code_prefix = str(row['코드'])[:2]

            # 해당 시도 코드에 해당하는 시군구 데이터 찾기
            matching_sigg = df2[df2['시군구코드'].astype(str).str.startswith(sido_code_prefix)]
            
            # 각 시군구 데이터에 대해 INSERT 문 실행
            for _, sigg_row in matching_sigg.iterrows():
                sql = "INSERT INTO `sigg_areas` (`id`, `sido_area_id`, `name`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (sigg_row['시군구코드'], row['코드'], sigg_row['시도_시군구']))

    # 변경 사항 저장
    conn.commit()
finally:
    conn.close()  # 데이터베이스 연결 닫기