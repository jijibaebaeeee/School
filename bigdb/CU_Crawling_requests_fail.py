import requests
from bs4 import BeautifulSoup

url = "https://cu.bgfretail.com/product/product.do?category=product&depth2=4&sf=N"

webpage = requests.get(url)  # URL에서 웹 페이지 가져오기
soup = BeautifulSoup(webpage.content, "html.parser") # BeautifulSoup을 사용하여 HTML 파싱
# < 카테고리 >
category_ul = soup.find('ul', class_='prodInfo') # 'ul' 태그 중 'prodInfo' 클래스를 가진 요소 찾기
products = soup.find_all('li', class_='prod_list')
print(products)
# print(category_div)
# 결과 추출 (오직 'text'만)
# 추출할 것이 있다면
if category_ul:
    category_texts = [li.get_text(strip=True) for li in category_ul.find_all('li')]
else:
    category_texts = []

# 각 제품의 정보 추출
product_info = []
for product in products:
    name = product.find('div', class_='name').get_text(strip=True) if product.find('div', class_='prodListWrap') else 'No name'
    price = product.find('div', class_='price').get_text(strip=True) if product.find('div', class_='price') else 'No price'
    product_info.append({'name': name, 'price': price})

print(product_info)

print(category_texts)



# webpage = requests.get(url) # url 객체 저장
# soup = BeautifulSoup(webpage.content, "html.parser") # 해당 url의 html 가져옴

# category = soup.find_all('ul','prodInfo')
# item_name = soup.find_all('div','name')
# price = soup.find_all('div','price')

# #html = category.text
# #psr = BeautifulSoup(html,"html.parser")
# #print(html)

# category_2 = soup.select('.prodInfo_02 a')
# print(category_2)
# print(category)

#tmp = category.text
#print(tmp)

#category_list = [soup.find_all('li','prodInfo')[n].a.string for n in range(0, len(category))]
#print(category_list)


#category.append(soup.find_all())
#print(category)

# 결과 추출
# 'category_ul'이 None이 아닐 경우에만 내부의 'li' 태그 추출
# if category_ul:
#     categories = [{'text': li.get_text(strip=True), 'link': li.a['href']} for li in category_ul.find_all('li')]
# else:
#     categories = []

# print(categories)

