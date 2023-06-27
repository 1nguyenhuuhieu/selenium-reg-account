from selenium import webdriver
from selenium.webdriver.common.by import By

import time


proxy_server = '171.234.58.26:25373'

def init_driver(proxy_server):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=' + proxy_server)
    driver = webdriver.Chrome(options=chrome_options)

    return driver


if __name__ == "__main__":
    driver = init_driver(proxy_server)
    time.sleep(2)

    driver.get('https://www.69vn1.com/')
    time.sleep(2)
