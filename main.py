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
import configparser
import pandas as pd
import sys
from urllib.parse import urlparse
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService

url_new_proxy = "https://tmproxy.com/api/proxy/get-new-proxy"
url_current_proxy = "https://tmproxy.com/api/proxy/get-current-proxy"
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract



config = configparser.ConfigParser()
config.read('config.ini')

tmp_proxy_apikey = config.get('DEFAULT', 'api_key')
file_user_path = config.get('DEFAULT', 'user_info')
file_webs_path = config.get('DEFAULT', 'webs')

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


# Random username
def generate_username():
    first_name_list = ["red", "blue", "green", "orange",
                       "white", "black", "yellow", "purple", "silver", "brown"]

    username = random.choice(first_name_list) + str(random.randint(1000, 9999))
    username = username.lower()

    return username


class UserInfo:
    def __init__(self, name, phone, bank_account, bank_branch):
        clear_name = no_accent_vietnamese(name)
        self.name = clear_name.upper()
        self.username = generate_username()
        self.phone = phone
        self.bank_account = bank_account
        self.bank_branch = bank_branch
        self.pwd_login = generate_password()
        self.pwd_money = str(random.randint(10000000, 100000000))

def init_driver(proxy_server):
    chrome_driver_path = 'chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--ignore-certificate-errors')
    if proxy_server:
        chrome_options.add_argument('--proxy-server=' + proxy_server)
    else:
        print("Sử dụng IP thật")
    service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def file_to_list(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
        content = [line.strip() for line in content]
    return content


def get_users_from_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    sql = '''SELECT * FROM users WHERE (is_addbank is NULL) OR is_addbank = 0'''
    users = cursor.execute(sql).fetchall()
    return users

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
                        phone TEXT,
                        is_addbank BOOLEAN
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
        phone,
        is_addbank
        ) VALUES (?,?,?,?,?,?,?,?,?,?)""", (now,
                                        user.username,
                                        user.pwd_login,
                                        user.pwd_money,
                                        url_web,
                                        user.bank_account,
                                        user.bank_branch,
                                        user.name,
                                        user.phone,
                                        False
                                        ))
    # Commit the changes
    conn.commit()
    print('SAVE RECORD TO DATABASE DEBUG 4')
    # Close the cursor and the database connection
    cursor.close()
    conn.close()
    return None
    
def update_user_to_database(user, logic):
    # Connect to the database (create a new one if it doesn't exist)
    conn = sqlite3.connect('database.db')
    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET is_addbank = ? WHERE username = ?""", (logic, user['username']))
    # Commit the changes
    conn.commit()
    # Close the cursor and the database connection
    cursor.close()
    conn.close()
    



def get_element(parrent, tag_name, attribute_name, value):
    try:
        elms = WebDriverWait(parrent, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, tag_name)) 
        for elm in elms:
            if elm.get_attribute(attribute_name) == value:
                return elm
        
        return None
    except:
        return None

    
def fill_register_form(driver, user):
    
    form_submit = get_element(driver, 'form', 'ng-submit', '$ctrl.submit()')
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
        
        fill_captcha(form_submit)

    return None

def fill_login_form(form_login, user):
    try:
        username = user['username']
        pwd_login = user['pwd_login']
        inputs = form_login.find_elements(By.TAG_NAME, 'input')
        for input in inputs:
            if input.get_attribute('ng-model') == '$ctrl.user.account.value':
                input.send_keys(username)
            if input.get_attribute('ng-model') == '$ctrl.user.password.value':
                input.send_keys(pwd_login)
        fill_captcha(form_login)
    except:
        pass
    
    
    
    return True



# Open register form
# option = '$ctrl.styles.reg' --> Register
# option = '$ctrl.styles.login' --> Login
def open_form(driver, url_register, option):
    if option == 'reg':
        value = '$ctrl.styles.reg'
    else:
        value = '$ctrl.styles.login'
    driver.get(url_register)
    time.sleep(2)
    # Click close button
    close_button = get_element(driver, "button", "ng-click", "$ctrl.ok()") or get_element(driver, "span", "ng-click", "$ctrl.ok()")
    while close_button:
        close_button.click()
        time.sleep(1)
        close_button = get_element(driver, "button", "ng-click", "$ctrl.ok()") or get_element(driver, "span", "ng-click", "$ctrl.ok()")
        time.sleep(1)

    button = get_element(driver, 'button', 'ng-class', value)

    if button:
        button.click()
        return True

    return False


def login(driver, user):
    url = user['url_web']
    driver.get(url)
    time.sleep(3)
    # Click close button
    close_button = get_element(driver, "button", "ng-click", "$ctrl.ok()") or get_element(driver, "span", "ng-click", "$ctrl.ok()")
    while close_button:
        close_button.click()
        time.sleep(1)
        close_button = get_element(driver, "button", "ng-click", "$ctrl.ok()") or get_element(driver, "span", "ng-click", "$ctrl.ok()")
        time.sleep(1)
        
    time.sleep(3)
    
    form_login = get_element(driver, 'form', 'ng-submit', '$ctrl.login()')
    limit_try = 5
    while limit_try > 0 and not form_login:
        open_form(driver, url, 'login')
        time.sleep(3)
        form_login = get_element(driver, 'form', 'ng-submit', '$ctrl.login()')
        
    limit_try = 3
    is_login_success =  False
    while limit_try > 0 and not is_login_success:
        limit_try -= 1
        fill_login_form(form_login, user)
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        is_login_success =  get_element(driver, 'span', 'ng-class', '$ctrl.styles.account')
            
def append_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content + '\n')

def fill_captcha(form_submit):
    captcha_input = get_element(form_submit, 'input', 'ng-model', '$ctrl.code')
    if captcha_input:
        captcha_input.click()
        time.sleep(2)
        img_captcha = get_element(form_submit, 'img', 'ng-class', '$ctrl.styles.captcha')
        if img_captcha:
            data_url = img_captcha.get_attribute('src')
            img = load_image_from_base64(data_url)
            text = pytesseract.image_to_string(img)
            text = text[0:4]
            captcha_input.send_keys(text)
            form_submit.submit()
            time.sleep(1)
            
    return None
            
def auto_register(url_web, user_info):
    proxy_server = get_proxy()
    driver = init_driver(proxy_server)
    print(f'Khởi tạo driver mới, proxy: {proxy_server}')
    print(f'{url_web} --- Bắt đầu đăng kí tài khoản: {user_info["name"]}. Số tài khoản: {user_info["bank_account"]}')
    
    limit_try = 3
    is_open_register_form = False
    while limit_try > 0 and not is_open_register_form:
        is_open_register_form = open_form(driver, url_web, 'reg')
        limit_try -= 1
        
    # Open register form success    
    if is_open_register_form:
        try:
            is_register_success = False
            limit_try = 10
            while limit_try > 0 and not is_register_success:
                open_form(driver, url_web, 'reg')
                limit_try -= 1
                try:
                    user = UserInfo(user_info['name'],
                                    str(user_info['phone']),
                                    str(user_info['bank_account']),
                                    user_info['bank']
                                    )
                    fill_register_form(driver, user)
                    time.sleep(2)
                    is_register_success = not get_element(driver, 'button', 'ng-class', '$ctrl.styles.reg')
                    if is_register_success:
                        print(f'{url_web} --- Đăng kí thành công tài khoản {user.username}, mật khẩu đăng nhập: {user.pwd_login}, mật khẩu rút tiền: {user.pwd_money}')
                        time.sleep(2)
                        # saved to database
                        try:
                            print('Try to save to database')	
                            save_record_to_database(user, url_web)
                        except:
                            print('Except to save to database')
                            pass
                        break
                    time.sleep(2)
                except:
                    pass
        except:
            now = datetime.now()
            now = now.strftime("%d/%m/%Y %H:%M")
            print(f'Lỗi khi đăng ký: {url_web}')
            log = f"Timestamp: {now}; Web: {url_web}; Name: {user_info['name']}; Phone: {user_info['phone']}; Bank Account: {user_info['bank_account']}; Bank Branch: {user_info['bank']}"
            file_path = 'errors.txt'
            append_to_file(file_path, log)
        driver.quit()
        time.sleep(2)

def auto_add_bank(user_info):
    proxy_server = get_proxy()
    driver = init_driver(proxy_server)
    url_web = user_info['url_web']
    print(f'Khởi tạo driver mới, proxy: {proxy_server}')
    print(f'{url_web} --- Bắt đầu thêm thông tin ngân hàng tài khoản: {user_info["name"]}. Số tài khoản: {user_info["bank_account"]}')

    login(driver, user_info)
    
    time.sleep(2)
        
    try:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc
        add_bank_url = base_url + '/WithdrawApplication'
        driver.get(add_bank_url)
        time.sleep(3)
        form_addbank = get_element(driver, 'form','ng-submit', '$ctrl.onBankAccountSubmit()')
        if form_addbank:
            select_bank = get_element(form_addbank, 'select', 'ng-model',"$ctrl.viewModel.bankAccountForm.bankName.value")
            select = Select(select_bank)
            select.select_by_visible_text('MBBANK')
            bank_branch = get_element(form_addbank, 'input', 'ng-model',"$ctrl.viewModel.bankAccountForm.city.value")
            bank_account = get_element(form_addbank, 'input', 'ng-model',"$ctrl.viewModel.bankAccountForm.account.value")

            bank_branch.send_keys(user_info['bank_branch'])
            bank_account.send_keys(user_info['bank_account'])
            
            time.sleep(2)
            form_addbank.submit()
            time.sleep(2)
            update_user_to_database(user, True)
        else:
            update_user_to_database(user, False)
    except:
        update_user_to_database(user, False)
    driver.quit()
    time.sleep(2)
    
        
if __name__ == "__main__":
    mode = sys.argv[1]

    if mode == 'reg':
        users = excel_to_dictionary(file_user_path)
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
    elif mode == 'add_bank':
        users = get_users_from_database()
        for user in users:
            auto_add_bank(user)
            time.sleep(2)
        
