from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys # 키 조작을 위해
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException #요소가 페이지에 없을 때
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains


import time #대기시간 지연
import csv
import pandas as pd
from tqdm import tqdm

# 1. 웹드라이버 초기화
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options) #wedriver 설치 경로

#CU편의점 url
URL = "https://cu.bgfretail.com/product/product.do?category=product&depth2=4&sf=N"
driver.get(URL) #웹페이지 열기
time.sleep(1) #대기

product_names,product_prices, product_sub, product_main = [], [], [], []

#main, sub 카테고리별 딕셔너리 정의
MAINCATEGORY={
    '10':'간편식사',
    '20':'즉석조리',
    #'30':'과자류',
    #'40':'아이스크림',
    #'50':'식품',
    #'60':'음료',
#    '70':'생활용품',
}

SUBCATEGORY={
    '10':{'도시락','샌드위치/햄버거','주먹밥/김밥'},
    '20':{'튀김류','베이커리','즉석커피'},
    #'30':{'스낵/비스켓','빵/디저트','껌/초콜릿/캔디'},
    #'40':{'아이스크림'},
    #'50':{'가공식품','안주류','식재료'},
    #'60':{'음료','아이스드링크','유제품'},
#    '70':{'취미/레저','의약외품','신변잡화','생활 잡화'}
}

# def scroll_to_element(element):
#     actions = ActionChains(driver)
#     actions.move_to_element(element).perform()

def click_element_with_js(element):
    driver.execute_script("arguments[0].click();", element)

# [code 4] 더보기 클릭
def clickMore():
    for i in range(1):
        driver.execute_script("nextPage(1)")
        time.sleep(2)

# [code2]메인 카테고리 분류 
def goMain(category):
    script="" #초기화
    if category =='10': #간편식사
        script = "gomaincategory('{}', 1)".format(category)
    elif category == '20': #즉석조리
        script = "gomaincategory('{}', 2)".format(category)
    elif category == '30': #과자류
        script = "gomaincategory('{}', 3)".format(category)
    elif category == '40': #아이스크림
        script = "gomaincategory('{}', 4)".format(category)
    elif category == '50': #식품
        script = "gomaincategory('{}', 5)".format(category)
    elif category == '60': #음료
        script = "gomaincategory('{}', 6)".format(category)
#     elif category == '70':#생활용품 
#         script = "gomaincategory('{}', 7)".format(category)
    else:
        script = "gomaincategory('{}', 1)".format(category)

    driver.execute_script(script) #스크립트 실행
    time.sleep(2)

#[code 3]goSub함수 #파이썬 스크롤 사용
# def goSub(num):
#     class_format="eventInfo_{:02d}".format(num) #문자열포맷팅
#     #현재 HTML에서 해당 클래스가 존재하는지 확인
#     try:
#         driver.find_element(By.CLASS_NAME, class_format)
#     except NoSuchElementException:
#         print('NO')
#         return 
#     #클래스가 존재하는 경우 
#     li_element = driver.find_element(By.CLASS_NAME, class_format)
#     a_element = li_element.find_element(By.TAG_NAME, "a")
#     scroll_to_element(a_element)
#     a_element.click()
#     time.sleep(1)

#goSub 함수 자바스크립트 사용
def goSub(num):
    class_format = "eventInfo_{:02d}".format(num)  # 문자열포맷팅
    # 현재 HTML에서 해당 클래스가 존재하는지 확인
    try:
        li_element = driver.find_element(By.CLASS_NAME, class_format)
        # 클래스가 존재하는 경우 
        a_element = li_element.find_element(By.TAG_NAME, "a")
        click_element_with_js(a_element)  # JavaScript를 사용하여 클릭
    except NoSuchElementException:
        print(f'Element with class {class_format} not found.')
    except Exception as e:
        print(f'Error while trying to click sub category: {e}')
    time.sleep(1)

#getSubCategoryNumber
def getSubCategoryNumber(main_cat, sub_cat):
    # 메인 카테고리에 해당하는 서브 카테고리 목록을 가져옵니다.
    sub_category_list = list(SUBCATEGORY[main_cat])

    # 서브 카테고리의 이름을 기반으로 인덱스를 찾아 반환합니다.
    # 인덱스는 0부터 시작하지만, 웹사이트에서는 1부터 시작하는 번호를 사용할 수도 있으므로 +1을 해줍니다.
    return sub_category_list.index(sub_cat) + 1

# [code 5] 상품 정보 가져오기
def getProductInfo(soup, main, sub, products):
    li_element = soup.find_all('li', class_='prod_list')
    for li in li_element:
        name_element = li.select_one('div.prod_text > div.name > p')
        product_name = name_element.text.strip()
        price_element = li.select_one('div.prod_text > div.price > strong')
        product_price = price_element.text.strip()

        # 제품 정보를 리스트에 추가
        products.append({
            'name': product_name,
            'price': product_price,
            'main_category': main,
            'sub_category': sub
        })
        time.sleep(0.3)


category_data = {}

try:
    #4. 데이터 프레임 생성
    df = pd.DataFrame({
        '메인분류': product_main,
        '서브분류': product_sub,
        '상품명': product_names,
        '가격': product_prices
    })

    for main_cat, main_name in MAINCATEGORY.items():
        print(f"Processing main category: {main_name}")
        goMain(main_cat)
        sub_categories = SUBCATEGORY[main_cat]

        # 메인 카테고리에 대한 딕셔너리 초기화
        category_data[main_name] = {}

        for sub_cat in SUBCATEGORY[main_cat]:
            print(f"Processing sub category: {sub_cat}")
            sub_cat_num = getSubCategoryNumber(main_cat, sub_cat)  # 메인 카테고리와 서브 카테고리 인자 전달
            goSub(sub_cat_num)
            #clickMore()
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 서브 카테고리의 제품 정보를 담을 리스트 초기화
            products = []
            getProductInfo(soup, main_name, sub_cat, products)

            # 서브 카테고리에 대한 제품 정보 저장
            category_data[main_name][sub_cat] = products

    # 크롤링이 완료된 후 결과 출력
    print("Crawling completed. Printing results...")
    for main_cat, sub_cats in category_data.items():
        print(f"Main Category: {main_cat}")
        for sub_cat, products in sub_cats.items():
            print(f"  Sub Category: {sub_cat}")
            for product in products:
                # 제품 이름과 가격을 함께 출력
                print(f"Product Name: {product['name']}, Price: {product['price']}")
    # category_data 딕셔너리를 이용하여 DataFrame 생성
    rows = []
    for main_cat, sub_cats in category_data.items():
        for sub_cat, products in sub_cats.items():
            for product in products:
                rows.append({
                    '메인분류': main_cat,
                    '서브분류': sub_cat,
                    '상품명': product['name'],
                    '가격': product['price']
                })

    df = pd.DataFrame(rows)

    #매핑
    # category_map = {'간편식사': 'a', '즉석조리': 'b', '과자류': 'c', '아이스크림': 'd', '식품': 'e', '음료': 'f'}
    # df['ID'] = df['메인분류'].map(category_map)
    # df['그룹별INDEX']=df.groupby('ID').cumcount()+1
    # df['ID']=df['ID']+df['그룹별INDEX'].astype(str)
    # df.set_index('ID',inplace=True)
    # #그룹별 INDEX 칼럼 삭제
    # df.drop('그룹별INDEX',axis=1,inplace=True) #axis=1 열 
    # df.shape[0] #전체 데이터 개수
    # df.tail(10)

    # df['가격'] = df['가격'].str.replace(',', '')  # 콤마(,) 제거
    # df['가격'] = df['가격'].astype(int)  # int 형식으로 변환

    # # DataFrame을 CSV 파일로 저장
    # df.to_csv('./편의점크롤링.csv', index=False, encoding='cp949', mode = 'w')
    # DataFrame에 추가 변경사항 적용

    # 다시 돌아가고 싶으면 여기 주석 푸셈
    # category_map = {'간편식사': 'a', '즉석조리': 'b'}#, '과자류': 'c', '아이스크림': 'd', '식품': 'e', '음료': 'f'}
    # df['ID'] = df['메인분류'].map(category_map)
    # df['그룹별INDEX'] = df.groupby('ID').cumcount() + 1
    # df['ID'] = df['ID'] + df['그룹별INDEX'].astype(str)
    # df['가격'] = df['가격'].astype(str).str.replace(',', '')
    # df['가격'] = df['가격'].astype(int)  # int 형식으로 변환

    # # 여기서 set_index를 사용하지 않고, 'ID' 열을 유지합니다.
    # df.set_index('ID', inplace=True)
    # df.drop('그룹별INDEX', axis=1, inplace=True)
    # df.shape[0]
    # #df.drop('그룹별INDEX', axis=1, inplace=True)

    # # 변경사항을 적용한 DataFrame을 CSV 파일로 저장
    # df.to_csv('./편의점크롤링.csv', index=False, encoding='cp949')

    # # 저장된 CSV 파일 확인
    # df = pd.read_csv('./편의점크롤링.csv', encoding='cp949')
    # print(df.tail(10))
   


except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()

category_map = {'간편식사': 'a', '즉석조리': 'b'}#, '과자류': 'c', '아이스크림': 'd', '식품': 'e', '음료': 'f'}
df['ID'] = df['메인분류'].map(category_map)
df['그룹별INDEX'] = df.groupby('ID').cumcount() + 1
df['ID'] = df['ID'] + df['그룹별INDEX'].astype(str)

# 여기서 set_index를 사용하지 않고, 'ID' 열을 유지합니다.
df.set_index('ID', inplace=True)
df.drop('그룹별INDEX', axis=1, inplace=True)
df.shape[0]
#df.drop('그룹별INDEX', axis=1, inplace=True)
df['가격'] = df['가격'].astype(str).str.replace(',', '')
df['가격'] = df['가격'].astype(int)  # int 형식으로 변환

# 변경사항을 적용한 DataFrame을 CSV 파일로 저장
df.to_csv('./편의점크롤링.csv', encoding='cp949')

# 저장된 CSV 파일 확인
df = pd.read_csv('./편의점크롤링.csv', encoding='cp949')
print(df.tail(10))

# df = pd.DataFrame({
#     '메인분류': product_main,
#     '서브분류': product_sub,
#     '상품명': product_names,
#     '가격': product_prices
# })

# df.tail(20)

# #df.to_csv('./편의점크롤링.csv',index=False, encoding='cp949',mode='w')

# df = pd.read_csv('./편의점크롤링.csv',encoding='cp949')
# df.tail(10)

# main_category=df['메인분류'].unique() #메인분류 값 확인 
# print(main_category)

# #매핑
# category_map = {'간편식사': 'a', '즉석조리': 'b', '과자류': 'c', '아이스크림': 'd', '식품': 'e', '음료': 'f'}
# df['ID'] = df['메인분류'].map(category_map)
# df['그룹별INDEX']=df.groupby('ID').cumcount()+1
# df['ID']=df['ID']+df['그룹별INDEX'].astype(str)
# df.set_index('ID',inplace=True)
# #그룹별 INDEX 칼럼 삭제
# df.drop('그룹별INDEX',axis=1,inplace=True) #axis=1 열 
# df.shape[0] #전체 데이터 개수
# df.tail(10)

# df['가격'] = df['가격'].str.replace(',', '')  # 콤마(,) 제거
# df['가격'] = df['가격'].astype(int)  # int 형식으로 변환

# df.to_csv('./편의점크롤링.csv',encoding='cp949',mode='w')