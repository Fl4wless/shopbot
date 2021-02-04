from bs4 import BeautifulSoup
from selenium import webdriver
import ezgmail, time, requests
from info import *
from selenium.webdriver.common.by import By


url = 'https://eshop.ciernediery.sk/'
headers = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
sender_email = os.environ.get('MAIL_USERNAME')
recipient = 'runefinity@gmail.com'
password = os.environ.get('MAIL_PASSWORD')

PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)


def send_notification_in_stock(recipient, buy_link):
    ezgmail.send(recipient, 'Cierne diery - in stock', buy_link)

def fltr(item):
    return 'product_cat-trnava' in item['class']

def scan_site():
        req = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(req.content, 'html.parser')
        riso = soup.find_all('li', class_='product_cat-citanie')
        return riso

in_stock = list(filter(fltr, scan_site()))

def get_link():
    for item in in_stock:
        links = item.find_all('a', class_='product_type_simple')
        buy_now = links[1]
        return str(buy_now)

def get_clean_url(link):
    l = link.split(' ')
    url = l[2].split('"')
    return(url[1])

def fill_form(form, info):
    driver.find_element_by_name(form).send_keys(info)


def place_order(url):
    driver.get(url)
    fill_form('billing_first_name', FIRST)
    fill_form('billing_last_name', LAST)
    fill_form('billing_phone', PHONE)
    fill_form('billing_email', EMAIL)
    fill_form('billing_address_1', ADDRESS_1)
    fill_form('billing_address_2', ADDRESS_2)
    fill_form('billing_postcode', ZIP)
    fill_form('billing_city', CITY)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//*[@id="payment"]/div/p[1]/label/span[1]'))
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//*[@id="payment"]/div/p[2]/label/span[1]'))
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID, 'place_order'))


while True:
    in_stock = list(filter(fltr, scan_site()))
    if in_stock:
        link_with_tags = get_link()
        clean_link = get_clean_url(link_with_tags)
        send_notification_in_stock('runefinity@gmail.com', clean_link)
        place_order(clean_link)
        time.sleep(2)
        break
    print('next loop in 30')
    time.sleep(30)

