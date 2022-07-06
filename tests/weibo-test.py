from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
server="http://localhost:4723/wd/hub"
desired_caps = {
  "platformName": "Android",
  "platformVersion": "9",
  "deviceName": "f978cc97",
  "appPackage": "com.sina.weibo",
  "appActivity": "com.sina.weibo.MainTabActivity",
  "automationName": "UiAutomator2",
  "noReset": "True"
}
driver=webdriver.Remote(server,desired_caps)
time.sleep(10)

descs = driver.find_element_by_id("com.sina.weibo:id/contentTextView")
print(descs.get_attribute("content-desc"))
print(descs.text)

el2 = driver.find_element_by_accessibility_id("首页")
el2.click()

time.sleep(100000)