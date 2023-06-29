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
from datetime import datetime
import sqlite3
import pandas as pd
import requests
import multiprocessing as mp
tmp_proxy_apikey = 'a37a0d79fe6df60b9ffc7b3eec6de257'
url_new_proxy = "https://tmproxy.com/api/proxy/get-new-proxy"
url_current_proxy = "https://tmproxy.com/api/proxy/get-current-proxy"
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract



def get_proxy():
    new_proxy_json = {
    "api_key": tmp_proxy_apikey,
    "sign": "string",
    "id_location": 0
    }
    current_proxy_json = {
    "api_key": tmp_proxy_apikey
    }
    r = requests.post(url_new_proxy, json=new_proxy_json)
    if r.json()['data']['https']:
        proxy =  r.json()['data']['https']
        return proxy
    else:
        r = requests.post(url_current_proxy, json=current_proxy_json)
        if r.json()['data']['https']:
            proxy =  r.json()['data']['https']
            return proxy
        else:
            print("Lỗi, không lấy được proxy")
            return None
        
def excel_to_dictionary(file_path):
    df = pd.read_excel(file_path)  # Read the Excel file
    data = df.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries
    return data

def load_image_from_base64(data_url):
    # Extract the base64 encoded image data
    _, base64_data = data_url.split(',', 1)
    # Decode the base64 data
    image_data = base64.b64decode(base64_data)
    # Create a BytesIO object to load the image data
    image_buffer = BytesIO(image_data)
    # Open the image using PIL
    image = Image.open(image_buffer)
    return image

def generate_password(length=8):
    characters = string.ascii_letters
    password = ''.join(random.choice(characters) for _ in range(length))
    password += '@aA0'
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
        self.username = generate_username(clear_name.lower())
        self.phone = phone
        self.bank_account = bank_account
        self.bank_branch = bank_branch
        self.pwd_login = generate_password()
        self.pwd_money = str(random.randint(10000000, 100000000))

def init_driver(proxy_server):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    if proxy_server:
        chrome_options.add_argument('--proxy-server=' + proxy_server)
    else:
        print("Sử dụng IP thật")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def file_to_list(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
        content = [line.strip() for line in content]
    return content

def save_record_to_database(user, url_web):
    now = datetime.now()
    # Connect to the database (create a new one if it doesn't exist)
    conn = sqlite3.connect('database.db')
    # Create a cursor object
    cursor = conn.cursor()
    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        time_created DATETIME,
                        username TEXT,
                        pwd_login TEXT,
                        pwd_money TEXT,
                        url_web TEXT,
                        bank_account TEXT,
                        bank_branch TEXT,
                        name TEXT,
                        phone TEXT
                    )''')
    # Insert the record into the table
    cursor.execute("""INSERT INTO users (
        time_created,
        username,
        pwd_login,
        pwd_money,
        url_web,
        bank_account,
        bank_branch,
        name,
        phone
        ) VALUES (?,?,?,?,?,?,?,?,?)""", (now,
                                        user.username,
                                        user.pwd_login,
                                        user.pwd_money,
                                        url_web,
                                        user.bank_account,
                                        user.bank_branch,
                                        user.name,
                                        user.phone))
    # Commit the changes
    conn.commit()
    # Close the cursor and the database connection
    cursor.close()
    conn.close()
def click_element(driver, tag_name, attribute_name, value):
    try:
        elms = WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, tag_name)) 
        for elm in elms:
            if elm.get_attribute(attribute_name) == value:
                try:
                    elm.click()
                except:
                    pass
                time.sleep(2)
                return True
    except:
        return False
def fill_register_form(driver, user):
    form_submit = None
    forms = driver.find_elements(By.TAG_NAME, 'form')
    for form in forms:
        if form.get_attribute('ng-submit') == '$ctrl.submit()':
            form_submit = form
    if form_submit:
        inputs = form_submit.find_elements(By.TAG_NAME, 'input')
        for input in inputs:
            if input.get_attribute('ng-model') == '$ctrl.user.account.value':
                input.send_keys(user.username)
            if input.get_attribute('ng-model') == '$ctrl.user.password.value':
                input.send_keys(user.pwd_login)
            if input.get_attribute('ng-model') == '$ctrl.user.confirmPassword.value':
                input.send_keys(user.pwd_login)
            if input.get_attribute('ng-model') == '$ctrl.user.moneyPassword.value':
                input.send_keys(user.pwd_money)
            if input.get_attribute('ng-model') == '$ctrl.user.name.value':
                input.send_keys(user.name)
            if input.get_attribute('ng-model') == '$ctrl.user.mobile.value':
                input.send_keys(user.phone)
            if input.get_attribute('ng-model') == '$ctrl.code':
                input.click()
                time.sleep(2)
                imgs = form_submit.find_elements(By.TAG_NAME, 'img')
                for img in imgs:
                    if img.get_attribute('ng-class') == '$ctrl.styles.captcha':
                        data_url = img.get_attribute('src')
                        img = load_image_from_base64(data_url)
                        text = pytesseract.image_to_string(img)
                        text = text[0:4]
                        input.send_keys(text)
                        time.sleep(3)
                        form_submit.submit()
                        time.sleep(2)
                        break
    else:
            return False
def check_register_success(driver):
    driver.refresh()
    time.sleep(2)
    click_element(driver, "button", "ng-click", "$ctrl.ok()")
    click_element(driver, "span", "ng-click", "$ctrl.ok()")
    elms = WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, 'button')) 
    for elm in elms:
        if elm.get_attribute("ng-class") == "$ctrl.styles.reg":
            return False
    return True
def open_register_form(driver, url_register):
    driver.get(url_register)
    time.sleep(2)
    click_element(driver, "button", "ng-click", "$ctrl.ok()")
    click_element(driver, "span", "ng-click", "$ctrl.ok()")
    return click_element(driver, "button", "ng-class", "$ctrl.styles.reg")
def append_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content + '\n')
def auto_register(url_web, user_info):
    proxy_server = get_proxy()
    driver = init_driver(proxy_server)
    print(f'Khởi tạo driver mới, proxy: {proxy_server}')
    print(f'{url_web} --- Bắt đầu đăng kí tài khoản: {user_info["name"]}. Số tài khoản: {user_info["bank_account"]}')
    try:
        is_register_success = False
        limit_try = 10
        while limit_try > 0 and not is_register_success:
            open_register_form(driver, url_web)
            limit_try -= 1
            try:
                user = UserInfo(user_info['name'],
                                str(user_info['phone']),
                                str(user_info['bank_account']),
                                user_info['bank']
                                )
                fill_register_form(driver, user)
                time.sleep(2)
                is_register_success = check_register_success(driver) 
                if is_register_success:
                    print(f'{url_web} --- Đăng kí thành công tài khoản {user.username}, mật khẩu đăng nhập: {user.pwd_login}, mật khẩu rút tiền: {user.pwd_money}')
                    time.sleep(2)
                    # saved to database
                    try:
                        save_record_to_database(user, url_web)
                    except:
                        pass
                    break
                time.sleep(2)
            except:
                open_register_form(driver, url_web)
    except:
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M")
        print(f'Lỗi khi đăng ký: {url_web}')
        log = f"Timestamp: {now}; Web: {url_web}; Name: {user_info['name']}; Phone: {user_info['phone']}; Bank Account: {user_info['bank_account']}; Bank Branch: {user_info['bank']}"
        file_path = 'errors.txt'
        append_to_file(file_path, log)
    driver.quit()
    time.sleep(2)
if __name__ == "__main__":
    file_user_path = 'users.xlsx'
    users = excel_to_dictionary(file_user_path)
    file_webs_path = 'webs.txt'
    webs = file_to_list(file_webs_path)
    num_processes = len(webs)
    for user_info in users:
        arguments = []
        for web in webs:
            argument = (web, user_info)
            arguments.append(argument)
        pool = mp.Pool(processes=num_processes)
        pool.starmap(auto_register, arguments)
        pool.close()
        pool.join()