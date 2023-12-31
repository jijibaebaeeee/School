import pymysql
import pandas as pd
from db_setting import db

# 엑셀 파일 읽기
sigg_df = pd.read_excel('행정동 기준 시군구 단위.xlsx')
emd_df = pd.read_excel('행정동_코드_김홍시_.xlsx')

# 데이터베이스 연결
conn = pymysql.connect(host=db['host'], port=db['port'],
                       user=db['Username'], passwd=db['Password'],
                       db='store', charset='utf8mb4')

try:
    with conn.cursor() as cursor:
      
        cursor.execute("DELETE FROM emd_areas")

        for idx, emd_row in emd_df.iterrows():
            
            matching_sigg = sigg_df[sigg_df['시군구'] == emd_row['시군구명']]
            
            
            if not matching_sigg.empty:
                sigg_code = matching_sigg['시군구코드'].iloc[0]
                sql = "INSERT INTO `emd_areas` (`id`, `sigg_area_id`, `name`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (emd_row['행정동코드'], sigg_code, emd_row['읍면동명']))

    # 변경 사항 저장
    conn.commit()
finally:
    conn.close()  # 데이터베이스 연결 닫기