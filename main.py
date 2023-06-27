from selenium import webdriver
from selenium.webdriver.common.by import By
from io import BytesIO

from pytesseract import pytesseract
from PIL import Image
import requests




import time


proxy_server = '171.234.58.26:25373'
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

class UserInfo:
    def __init__(self):
        self.user = 'test256147'
        self.pwd = 'Matkhau@2023'
        self.pin_bank = '123456'
        self.name = 'Nguyễn Văn test'
        self.pin_bank = '123456'

def init_driver(proxy_server):

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server=' + proxy_server)
    driver = webdriver.Chrome(options=chrome_options)

    return driver


if __name__ == "__main__":
    driver = init_driver(proxy_server)
    time.sleep(2)

    driver.get('https://www.69vn1.com/')
    time.sleep(2)

    spans = driver.find_elements(By.TAG_NAME, "span")
    for span in spans:
        if span.text == 'Đóng':
            span.click()
            break
    time.sleep(2)

    spans = driver.find_elements(By.TAG_NAME, "span")
    for span in spans:
        if span.text == 'ĐĂNG KÝ':
            span.click()
            break
    time.sleep(2)
    for i in range(5):
        response = requests.get(image_path)
        img = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        text = text[:-1]
        text = text.lower()
        text = text.replace(" ","")
        texts.append(text)

    captcha_text = max(texts,key=texts.count)