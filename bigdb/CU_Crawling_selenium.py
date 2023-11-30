from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys # 키 조작을 위해
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException #요소가 페이지에 없을 때
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

import time #대기시간 지연

# 1. 웹드라이버 초기화
service = ChromeService(executable_path=ChromeDriverManager().install())   # chrome 최신 버전 유지
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install())) #wedriver 설치 경로

#CU편의점 url
URL = "https://cu.bgfretail.com/product/product.do?category=product&depth2=4&sf=N"
driver.get(URL) #웹페이지 열기
time.sleep(1) #대기

product_names,product_prices, product_sub, product_main = [], [], [], []

#main, sub 카테고리별 딕셔너리 정의
MAINCATEGORY={
    '10':'간편식사',
    '20':'즉석조리',
    '30':'과자류',
    '40':'아이스크림',
    '50':'식품',
    '60':'음료',
    '70':'생활용품',
}

SUBCATEGORY={
    '10':{'도시락','샌드위치/햄버거','주먹밥/김밥'},
    '20':{'튀김류','베이커리','즉석커피'},
    '30':{'스낵/비스켓','빵/디저트','껌/초콜릿/캔디'},
    '40':{'아이스크림'},
    '50':{'가공식품','안주류','식재료'},
    '60':{'음료','아이스드링크','유제품'},
    '70':{'취미/레저','의약외품','신변잡화','생활 잡화'}
}


# [code 4] 더보기 클릭
def clickMore():
    for i in range(5):
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

#[code 3]goSub함수
def goSub(num):
    class_format="eventInfo_{:02d}".format(num) #문자열포맷팅
    #현재 HTML에서 해당 클래스가 존재하는지 확인
    try:
        driver.find_element(By.CLASS_NAME, class_format)
    except NoSuchElementException:
        print('NO')
        return 
    #클래스가 존재하는 경우 
    li_element = driver.find_element(By.CLASS_NAME, class_format)
    a_element = li_element.find_element(By.TAG_NAME, "a")
    a_element.click()
    time.sleep(1)

# [code 5] 상품 정보 가져오기
def getProductInfo(soup,main,sub):
    #soup :html parser
    # list 추출
    li_element = soup.find_all('li', class_='prod_list')
    # list 만큼 반복
    for li in li_element:
        # 제품명 추출
        name_element = li.select_one('div.prod_text > div.name > p')
        product_name = name_element.text.strip() # 공백 제거
        product_names.append(product_name) #리스트에 담기
        # 제품가격 추출
        price_element = li.select_one('div.prod_text > div.price > strong')
        product_price = price_element.text.strip()
        product_prices.append(product_price)#리스트에 담기
        #메인,서브 카테고리 담기
        product_main.append(main)
        product_sub.append(sub)
        #대기
        time.sleep(0.3)


for main_cat, main_name in MAINCATEGORY.items():
    goMain(main_cat)  # 메인 카테고리 이동
    sub_categories = SUBCATEGORY[main_cat]  # 서브 카테고리 세트
    for sub_cat in sub_categories:
        # 여기서 sub_cat는 서브 카테고리의 이름입니다.
        # 필요한 경우 서브 카테고리에 해당하는 고유 번호나 추가 정보를 찾아서 사용해야 합니다.
        # 예를 들어, 서브 카테고리에 대한 고유 번호를 얻는 방법이 필요할 수 있습니다.
        # 이 예제에서는 단순화를 위해 서브 카테고리 이름을 직접 사용합니다.

        # 서브 카테고리 이동 (여기서는 서브 카테고리 번호가 필요합니다)
        # goSub(sub_num)  # 예: 서브 카테고리 번호가 필요함

        clickMore()  # '더보기' 클릭
        # 현재 페이지의 HTML 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        getProductInfo(soup, main_name, sub_cat)  # 상품 정보 수집

# 수집된 정보 출력
print(product_main)
print(product_sub)
print(product_names)
print(product_prices)


# 수집된 정보 출력
print(product_main)
print(product_sub)
print(product_names)
print(product_prices)