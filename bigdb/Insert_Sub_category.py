# CSV 파일을 불러옴
import pymysql
import pandas as pd
from db_setting import db

# file_path = '편의점크롤링.csv'
# data = pd.read_csv(file_path, encoding='cp949')

# # '서브분류' 열에서 고유한 값 추출
# unique_sub_categories = data['서브분류'].unique()

cate_a = ['샌드위치/햄버거','도시락','주먹밥/김밥']
cate_b = ['베이커리','튀김류','즉석커피']
cate_c = ['빵/디저트','껌/초콜릿/캔디','스낵/비스켓']
cate_d = ['아이스크림']
cate_e = ['가공식품','안주류','식재료']
cate_f = ['유제품','음료','아이스드링크']

# 데이터베이스에 연결
conn = pymysql.connect(host=db['host'], port=db['port'], 
                       user=db['Username'], passwd=db['Password'], 
                       db='store', charset='utf8mb4') 

try:
    main_id = 'f'
    with conn.cursor() as cursor:
        # 각 고유값에 대해 삽입 쿼리 실행
        for name in cate_f:
            sql = "INSERT INTO Sub_category (main_id, name) VALUES (%s, %s)"
            cursor.execute(sql, (main_id, name))

    # 변경 사항 저장
    conn.commit()
finally:
    conn.close()

print("데이터 삽입 완료")