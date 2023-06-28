from selenium import webdriver
from selenium.webdriver.common.by import By
from io import BytesIO

from pytesseract import pytesseract
from PIL import Image
from selenium.webdriver.support.wait import WebDriverWait

import base64

import random
import string

import time
import re

proxy_server = '171.234.58.26:25373'
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    password += '0'
    return password

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

def remove_spaces(string):
    return string.replace(" ", "")

def generate_username(name):
    username = ''
    name = name.lower()
    names = reversed(name.split(' '))
    for index, name in enumerate(names):
        if index == 0:
            username += name
        else:
            username += name[0]
    number =  random.randint(100, 1000)
    username += str(number)

    return username


class UserInfo:
    def __init__(self, name, phone, bank_account, bank_branch):
        clear_name = no_accent_vietnamese(name)

        self.name = clear_name.upper()

        self.phone = phone
        self.bank_account = bank_account
        self.bank_branch = bank_branch

        self.registed = []

    def get_username(self):
        name_lower = self.name.lower()
        return generate_username(name_lower)
    
    def get_pwd_login():
        return generate_password()
    
    def get_pwd_money():
        return random.randint(10000000, 100000000)

def init_driver(proxy_server):

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server=' + proxy_server)
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def init_webs(file_path):
    webs = []
    f = open(file_path)
    for line in f:
        webs.append(line)
    return webs
def init_user_info(file_path):
    users_info = []
    dataframe1 = dataframe.active
    for row in range(0, dataframe1.max_row):
        for col in dataframe1.iter_cols(1, dataframe1.max_column):
            print(col[row].value)
def fill_register_form(driver, user_info):
    username = user_info.get_username()
    pwd_login = user_info.get_pwd_login()
    pwd_money = user_info.get_pwd_money()
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    for input in inputs:
        if input.get_attribute('ng-model') == '$ctrl.user.account.value':
            input.send_keys(username)
        if input.get_attribute('ng-model') == '$ctrl.user.password.value':
            input.send_keys(pwd_login)
        if input.get_attribute('ng-model') == '$ctrl.user.confirmPassword.value':
            input.send_keys(pwd_login)
        if input.get_attribute('ng-model') == '$ctrl.user.moneyPassword.value':
            input.send_keys(pwd_money)
        if input.get_attribute('ng-model') == '$ctrl.user.name.value':
            input.send_keys(user_info.name)
        if input.get_attribute('ng-model') == '$ctrl.code':
            input.click()
            time.sleep(1)
            imgs = driver.find_elements(By.TAG_NAME, 'img')
            for img in imgs:
                if img.get_attribute('ng-class') == '$ctrl.styles.captcha':
                    base64_str = img.get_attribute('ng-src')
                    base64_img = base64_str.split(',')
                    base64_img = base64_img[1]
                    imgdata = base64.b64decode(base64_img)
                    img = Image.open(BytesIO(imgdata))
                    text = pytesseract.image_to_string(img)
                    text = text[0:4]
                    input.send_keys(text)
                    time.sleep(2)
                    form = driver.find_element(By.TAG_NAME, 'form')
                    form.submit()
                    time.sleep(10)
                    spans = driver.find_elements(By.TAG_NAME, 'span')
                    for span in spans:
                        if user_info.username in span.text:
                            return True
                    
                    return False

def open_register_form(driver, url_register):
    driver.get(url_register)
    time.sleep(2)
    try:
        btns = WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, "button")) 
        for btn in btns:
            if btn.get_attribute('ng-click') == '$ctrl.ok()':
                btn.click()
                time.sleep(1)
    except:
        pass
    try:
        spans = WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, "span")) 
        for span in spans:
            if span.get_attribute('ng-click') == '$ctrl.ok()':
                span.click()
                time.sleep(1)
    except:
        pass

    try:
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            if button.get_attribute('ng-class') == '$ctrl.styles.reg':
                button.click()
                return True
    except:
        return False

if __name__ == "__main__":
    time.sleep(2)
    users = []
    user_info = UserInfo('Nguyễn Văn Long Hải',97845165465,123456789,'haf noo')
    users.append(user_info)

    webs = init_webs('webs.txt')
    for user in users:
        print(f'Bắt đầu đăng kí tài khoản: {user.name}. Số tài khoản: {user.bank_account}')
        for url_web in webs:
            driver = init_driver(proxy_server)
            print(f'Khởi tạo driver mới, proxy: {proxy_server}')
            time.sleep(1)
            try:
                is_openned_register_form = open_register_form(driver, url_web)
                time.sleep(2)
                if is_openned_register_form:
                    is_register_success = False
                    limit_try = 5
                    while limit_try > 0 and not is_register_success:
                        print(f'Thử đăng kí lần {6-limit_try}')
                        is_register_success = fill_register_form(driver, user)
                        time.sleep(2)

            except:
                print(f'error web: {url_web}')
                pass
            
            print('Đăng kí thành công')
            driver.quit()
            time.sleep(2)