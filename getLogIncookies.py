from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from lxml import etree
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}
ch_options = webdriver.ChromeOptions()
ch_options.add_argument("start-maximized")
ch_options.add_argument("enable-automation")
# ch_options.add_argument("--headless")
ch_options.add_argument("--no-sandbox")
ch_options.add_argument("--disable-infobars")
ch_options.add_argument("--disable-dev-shm-usage")
ch_options.add_argument("--disable-browser-side-navigation")
ch_options.add_argument("--disable-gpu")

# 通过手动登录获取（更新）cookies 保持程序稳定运行
# 通过读取 cookies.json 加载 cookies


def makeCookies(driver):
    cookies = driver.get_cookies()
    with open("cookies.json", "w", encoding="utf-8") as cks:  # 从json文件中获取之前保存的cookie
        json.dump(cookies, cks)
    return True


def getCookies(driver):
    with open("cookies.json", "r", encoding="utf-8") as cks:  # 从json文件中获取之前保存的cookie
        cookies = json.load(cks)
    for cookie in cookies:
        driver.add_cookie(cookie)
    return True


if __name__ == '__main__':
    driver = webdriver.Chrome(options=ch_options)
    driver.get('https://www.bilibili.com/')
    input('输入以停止等待')
    makeCookies(driver)
