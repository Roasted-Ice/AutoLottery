import getLogIncookies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re
from lxml import etree
# 转发的动态地址 : https://t.bilibili.com/581846091538172544?tab=2

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


class LotteryRobot:
    currentDynamicId = ''
    UserId = ''

    def __init__(self, driver):
        driver.get('https://www.bilibili.com/')
        getLogIncookies.getCookies(driver)
        currentDynamicId = ''
        js = 'window.open("https://t.bilibili.com");'
        driver.execute_script(js)
        time.sleep(2)
        driver.close()
        self.SwitchWindow(driver, 1)
        self.UserId = driver.find_element_by_xpath(
            '//*[@class="user-name tc-black c-pointer"]').text
        print(self.UserId)
        # print(self.UserId.text)

    def getCardId(self, driver, i):
        Card_id = driver.find_elements_by_xpath(
            '//*[@class="card"]/a')[i-1]
        res_re = re.compile(r'(dynamicId_)([\d]+)')
        res = res_re.findall(Card_id.get_attribute('id'))[0][1]
        return res

    def getCurrentDynamicId(self, driver):
        lastCard_id = driver.find_element_by_xpath(
            '//*[@class="card"]/a')
        res_re = re.compile(r'(dynamicId_)([\d]+)')
        res = res_re.findall(lastCard_id.get_attribute('id'))[0][1]
        self.currentDynamicId = res
        print('==========  currentDynamicId:' + str(res)+'  ==============')

    def SwitchWindow(self, driver, i):
        windows = driver.window_handles
        driver.switch_to.window(windows[i-1])

    def TransDynamic(self, driver, dynamic_id):
        # 对当前页面进行判断是否含有抽奖符号
        time.sleep(2)
        trans_url = 'https://t.bilibili.com/{}?tab=1'.format(dynamic_id)
        driver.execute_script("window.open('{}')".format(trans_url))
        driver.switch_to.window(driver.window_handles[-1])
        # 判断是否是自己转发的内容
        UP_name = driver.find_element_by_xpath(
            '//*[@class="c-pointer"]').get_attribute('textContent')
        print(UP_name)
        if self.UserId == UP_name:
            print("是自己转发的,进行跳过")
            driver.close()
            self.SwitchWindow(driver, 1)
            return
        lottery_btn = ''
        try:
            # 检测是否是转发的抽奖动态
            # 判断转发的内容中的UP主是否关注了
            try:
                is_watched = driver.find_element_by_xpath(
                    '//*[@class="up-focus-btn"]').click()
            except Exception as e:
                print('已经关注过了')
                pass
            try:
                button = driver.find_elements_by_xpath(
                    '//*[@class="content-full"]')[1].click()
                self.SwitchWindow(driver, 3)
                time.sleep(1)
                print('是转发的动态')
                lottery_btn = driver.find_element_by_xpath(
                    '//*[@class="bp-svg-icon lottery-btn"]')
                trans_btn = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[2]/div/div/div/div[1]/div[4]/div[1]').click()
                if lottery_btn != '':
                    print('转发的是抽奖动态，冲冲冲!')
                    input_ = driver.find_element_by_xpath(
                        '//*[@class="textarea"]').send_keys('冲冲冲!')
                    time.sleep(1)
                    submit_button = driver.find_element_by_xpath(
                        '//*[@class="comm-submit f-right"]').click()
                driver.close()
                self.SwitchWindow(driver, 2)
                driver.close()
                self.SwitchWindow(driver, 1)
                return
            except Exception as e:
                print("转发的不是抽奖动态")
                driver.close()
                self.SwitchWindow(driver, 2)
                driver.close()
                self.SwitchWindow(driver, 1)
                # print(e)
                return
                pass
            lottery_btn = driver.find_element_by_xpath(
                '//*[@class="bp-svg-icon lottery-btn"]')
            print('是抽奖动态,冲冲冲')
        except:
            print('不是抽奖动态，进行跳过')
            pass

        if lottery_btn != '':
            input_ = driver.find_element_by_xpath(
                '//*[@class="textarea"]').send_keys('冲冲冲')
            # //*[@id="app"]/div/div[2]/div/div/div/div[4]/div/div[1]/div[1]/div[2]/textarea
            time.sleep(2)
            submit_button = driver.find_element_by_xpath(
                '//*[@class="comm-submit f-right"]').click()
        time.sleep(1)
        driver.close()
        self.SwitchWindow(driver, 1)

    def ListenNewDynamic(self, driver):
        # 更新 Card_id
        self.getCurrentDynamicId(driver)
        while True:
            # 初始循环等待
            driver.refresh()
            for i in range(1, 10):
                time.sleep(1)
                id = self.getCardId(driver, i)
                print(id)
                if id == self.currentDynamicId:
                    print("找到了上次的位置")
                    break
                self.TransDynamic(driver, id)
                if i % 5 == 0:
                    driver.execute_script(
                        "window.scrollTo(0,document.body.scrollHeight)")
            self.getCurrentDynamicId(driver)
            time.sleep(60)


if __name__ == '__main__':
    driver = webdriver.Chrome(options=ch_options)
    driver.implicitly_wait(2)
    robot = LotteryRobot(driver)
    robot.ListenNewDynamic(driver)
