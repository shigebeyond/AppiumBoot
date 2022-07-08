# http://www.ty2y.com/study/pythonappiumzdhslysypython3appiumsxzdsqzfbmyslnl.html

from appium import webdriver
import time
from appium.webdriver.common.touch_action import TouchAction

desired_caps = {
    "platformName": "Android",
    "platformVersion": "9",
    "deviceName": "f978cc97",
    "appPackage": "com.eg.android.AlipayGphone",
    "appActivity": "AlipayLogin",
    "noReset": "true",
    "fullReset": "false",
    "automationName": "UiAutomator1"
}

server = 'http://localhost:4723/wd/hub'
driver = webdriver.Remote(server, desired_caps)
time.sleep(2)
driver.find_element_by_id('com.alipay.android.phone.openplatform:id/more_app_icon').click() #点击更多
time.sleep(2)
driver.find_element_by_id('com.alipay.android.phone.wallet.homemarket:id/app_group_item_icon').click() #点击蚂蚁森林
time.sleep(2)

def Swipe(driver):
    n=0
    while n<=5:
        start_x = 500
        start_y = 1500
        distance = 1000
        driver.swipe(start_x, start_y, start_x, start_y - distance)
        n=n+1
    driver.find_element_by_xpath("//*[@text='查看更多好友']").click() #点击查看更多好友
    time.sleep(1)

def run(driver):
    Swipe(driver)
    while True:
        TouchAction(driver).press(x=150, y=700).release().perform() #第一个蚂蚁好友框框的坐标
        time.sleep(0.5)

        name = driver.find_element_by_id('com.alipay.mobile.nebula:id/h5_tv_title').text
        if name=='': #填写最后一个好友昵称
            driver.tap([(50, 130), (70, 150)], 100) #返回周排行榜主页( < 蚂蚁森林 )    driver.tap（x坐标,y坐标,t(ms)）
            time.sleep(1)
            driver.tap([(50, 130), (70, 150)], 100) #返回蚂蚁森林主页
            Swipe(driver)
            continue
        print('正在查看{0}'.format(name))
        items = driver.find_elements_by_class_name("android.widget.Button")
        if len(items)>5:
            for i in items:
                if '能量' in i.text:
                    print('收取{0}的{1}'.format(name,i.text.replace('收集','')))
                    i.click()

            time.sleep(0.5)
            driver.tap([(50, 130), (70, 150)], 100)
            time.sleep(0.1)

        start_x = 500
        start_y = 1910
        distance = 195  # 一个框的高度
        driver.swipe(start_x, start_y, start_x, start_y - distance)    # 向上滑动一个框的高度   # driver.swipe（分别表示滑动的起始和终点位置的 x/y 坐标）

        time.sleep(0.2)

if __name__ == '__main__':
    run(driver)
