# Project  : PySeTest
# FileName : MyHTMLTestRunner.py
# Author   : sugood
# DateTime : 2020/10/13 12:04
# Github   : https://github.com/sugood/PySeTest
# Version  : 1.0.0

#!/user/bin/env python
# -*-coding:utf-8-*-
import sys
import unittest
import datetime
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.chrome.options import Options

# 修改变量调整测试参数
home_url = 'http://www.mi.com/'
login_name = '输入账号'
login_pass = '输入密码'
test_product = "小米10 pro"

# 显示等待，通过标签ID定位
# param _driver: driver
# param _id: 需要查找的控件ID
# param timeout: 等待几秒
# param err_msg: 错误信息
# param finally_sleep: 有时候等待的结果显示已经找到元素了。但实际上使用的时候还是报错。所以，强制延时几秒
def webWaitById(_driver, _id, timeout, err_msg, finally_sleep=0):
    try:
        WebDriverWait(_driver, timeout).until(EC.visibility_of_element_located((By.ID, _id)))
    except TimeoutException:
        sys.exit(err_msg)
    finally:
        time.sleep(finally_sleep)

# 显示等待，通过Xpath和文本内容定位后并点击
# param _driver: driver
# param xpath: xpath
# param text: 查找的文本
# param timeout: 等待几秒
# param err_msg: 错误信息
# param finally_sleep: 有时候等待的结果显示已经找到元素了。但实际上使用的时候还是报错。所以，强制延时几秒
# param is_click: 是否点击找到的文本
def waitByTextAndClick(_driver, xpath, text, timeout, err_msg, finally_sleep=0, is_click = False):
    try:
        WebDriverWait(_driver, timeout).until( EC.text_to_be_present_in_element((By.XPATH, xpath), text))
    except TimeoutException:
        sys.exit(err_msg)
    finally:
        time.sleep(finally_sleep)

    if is_click:
        logger("点击："+text)
        _driver.find_element(By.XPATH,xpath).click()

# 定位列表并打开某项的链接
# param _driver: driver
# param xpath: xpath
# param position: 打开第几个链接
# param attribute: 默认为href，属性
def findListAndOpen(_driver, xpath, position, attribute = "href"):
    logger('打开第:' + str(position + 1) + "项的链接")
    _driver.get(_driver.find_elements(By.XPATH, xpath)[position].get_attribute(attribute))

# 自动填写文字到输入框
def auto_fill(driver, condition, context):
    # 首先定位到input，然后使用clear()
    driver.find_element(By.XPATH, condition).clear()
    # 往输入框写入内容类似
    driver.find_element(By.XPATH, condition).send_keys(context)

#alert 窗口确认
def alert_confirm(driver):
    # 等待弹出窗口出现
    WebDriverWait(driver, 10).until(alert_is_present())
    alertObject = driver.switch_to.alert  # 这里，alert方法不加括号，以为该方法被 @property 伪装成属性了，具体参考源码
    logger('弹出窗口内容---'+alertObject.text)  # text方法也被 @property 伪装成属性了
    alertObject.accept()  # 点击确定按钮

# 打印调试信息
def logger(log):
    time_stamp = datetime.datetime.now()
    print(time_stamp.strftime('%Y.%m.%d-%H:%M:%S ------')+log)

# 登录账号，并保存cookies
# param dirver
# param username: 用户名
# param password: 密码
def auto_login(driver, username, password):
    el = driver.find_element(By.XPATH, '//*[@id="J_siteUserInfo"]/a[1]')
    url=el.get_attribute("data-href")
    driver.get("https://"+url)
    webWaitById(driver, 'main-content', 5, "自动化测试失败:登录页打开超时")
    auto_fill(driver, '//input[@class="item_account" and @name="user"]', username)
    auto_fill(driver, '//input[@class="item_account" and @name="password"]', password)
    driver.find_element(By.XPATH, '//input[@id="login-button" and @class="btnadpt"]').click()
    webWaitById(driver, 'J_siteUserInfo', 5, "自动化测试失败:登录超时")
    cookie_items = driver.get_cookies()  # 獲取cookie值
    # 传入cookies
    for cookie in cookie_items:
        driver.add_cookie(cookie)

class TestIndex(unittest.TestCase):

    def setUp(self):
        is_headless = False  # True浏览器无界面模式,False有界面模式
        if(is_headless):
            chrome_options = Options()
            chrome_options.add_argument('window-size=1920x3000')
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome()

        self.driver.maximize_window()

    def testMain(self):
        driver = self.driver
        logger('开始自动化测试,首页测试...')
        driver.get(home_url)
        webWaitById(driver, 'J_siteUserInfo', 10, "自动化测试失败:首页打开超时")
        logger('开始登录...')
        auto_login(driver, login_name, login_pass)
        webWaitById(driver, 'J_siteUserInfo', 10, "自动化测试失败:返回首页超时")
        logger('输入搜索关键字测试')
        driver.find_element(By.ID, 'search').send_keys(test_product)
        logger('点击搜索')
        driver.find_element(By.XPATH, '//*[@id="J_submitBtn"]/input').click()
        webWaitById(driver, 'J_navCategory', 10, "自动化测试失败:打开搜索列表超时")
        findListAndOpen(driver,"//div[@class='goods-item']/div/a",0)
        waitByTextAndClick(driver, "//a[@class='btn btn-primary']", '加入购物车', 10, "自动化测试失败:打开产品失败",1, True)
        waitByTextAndClick(driver, "//a[@class='btn btn-primary']", '去购物车结算', 10, "自动化测试失败:加入购物车失败",1, True)
        waitByTextAndClick(driver, "//a[@class='btn btn-a btn-primary']", '去结算', 10, "自动化测试失败:去购物车结算失败",1)
        logger('输入商品数量')
        auto_fill(driver, '//input[@class="goods-num"]', 1)
        driver.find_element(By.XPATH, "//a[@class='btn btn-a btn-primary']").click()
        waitByTextAndClick(driver, "//a[@class='btn btn-primary']", '去结算', 10, "自动化测试失败:去结算失败",1)
        logger('选择第1个收货地址')
        driver.find_elements(By.XPATH, "//div[@class='address-item']")[0].click()
        waitByTextAndClick(driver, "//a[@class='btn btn-primary']", '立即下单', 10, "自动化测试失败:选中地址失败",1, True)
        waitByTextAndClick(driver, "//*[@class='fl']", '订单提交成功！去付款咯～', 10, "自动化测试失败:下单失败",1)
        logger('自动化测试成功')
    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
