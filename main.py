from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome('chromedriver')

title = []
price1 = ['0'] * 40
discount = ['0'] * 40
price2 = ['0'] * 40

url = 'https://www.digikala.com/incredible-offers/'
driver.get(url)
driver.find_element_by_class_name('c-product-list__content')
# scroll down
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, 'html.parser')
all_product = soup.find('div', class_='c-product-list__content')

c = 0
for product in all_product:
    title.append(product.findAll('div', class_='c-product-box__title')[1].text.
                 replace('\n','').replace('...', '').replace('\xa0','').strip())
    for item1 in product.findAll('div', class_='c-price__value'):
        for p1 in item1.find_all('del'):
            price1[c] = p1.text
        for p2 in item1.find_all('div', class_='c-price__value-wrapper'):
            price2[c] = p2.text.replace('\n','').strip()
    for item2 in product.findAll('div', class_='c-price__discount-oval'):
        for p3 in item2.find_all('span'):
            discount[c] = p3.text
    c += 1

# print(title)
# print(price1)
# print(discount)
# print(price2)
products = {'عنوان کالا': title,
            'قیمت اصلی': price1,
            'تخفیف': discount,
            'قیمت نهایی': price2,}
df = pd.DataFrame(products)
df.to_csv('product.csv')
