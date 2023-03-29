#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import sys
import os
import fnmatch
from pathlib import Path
import requests
from pyutilb import log, YamlBoot, BreakException, ocr_youdao
from pyutilb.util import *
import base64
from AppiumBoot.validator import Validator
from AppiumBoot.extractor import Extractor
# from AppiumBoot.helpers import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.action_chains import ActionChains

from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# 扩展WebElement方法
def get_text_or_content(self):
    r = self.text
    if r != '':
        return r
    return self.get_attribute("content-desc")
WebElement.get_text_or_content = get_text_or_content


# appium基于yaml的启动器
class Boot(YamlBoot):

    def __init__(self):
        super().__init__()
        # 动作映射函数
        actions = {
            'init_driver': self.init_driver,
            'close_driver': self.close_driver,
            'input_by_id': self.input_by_id,
            'input_by_aid': self.input_by_aid,
            'input_by_class': self.input_by_class,
            'input_by_xpath': self.input_by_xpath,
            'hide_keyboard': self.hide_keyboard,
            'swipe': self.swipe,
            'swipe_up': self.swipe_up,
            'swipe_down': self.swipe_down,
            'swipe_left': self.swipe_left,
            'swipe_right': self.swipe_right,
            'swipe_vertical': self.swipe_vertical,
            'swipe_horizontal': self.swipe_horizontal,
            'move_track': self.move_track,
            'drag_and_drop_by': self.drag_and_drop_by,
            'scroll_by': self.scroll_by,
            'move_by': self.move_by,
            'zoom_in': self.zoom_in,
            'zoom_out': self.zoom_out,
            'tap': self.tap,
            'tap_by': self.tap_by,
            'click_by': self.click_by,
            'click_by_if_exist': self.click_by_if_exist,
            'shake': self.shake,
            'set_orientation': self.set_orientation,
            'set_location': self.set_location,
            'screenshot': self.screenshot,
            'screenshot_element_by': self.screenshot_element_by,
            'execute_js': self.execute_js,
            'back': self.back,
            'enter': self.enter,
            'keyevent': self.keyevent,
            'open_notifications': self.open_notifications,
            'get_clipboard': self.get_clipboard,
            'set_clipboard': self.set_clipboard,
            'push_file': self.push_file,
            'pull_file': self.pull_file,
            'send_sms': self.send_sms,
            'print_performance': self.print_performance,
            'start_recording_screen': self.start_recording_screen,
            'stop_recording_screen': self.stop_recording_screen,
            'alert_accept': self.alert_accept,
            'alert_dismiss': self.alert_dismiss,
            'moveon_if_exist_by': self.moveon_if_exist_by,
            'break_if_exist_by': self.break_if_exist_by,
            'break_if_not_exist_by': self.break_if_not_exist_by,
            'base_url': self.base_url,
            'get': self.get,
            'post': self.post,
            'upload': self.upload,
            'download': self.download,
            'recognize_captcha': self.recognize_captcha,
            'recognize_captcha_element': self.recognize_captcha_element,
            'validate_by_jsonpath': self.validate_by_jsonpath,
            'validate_by_css': self.validate_by_css,
            'validate_by_xpath': self.validate_by_xpath,
            'validate_by_id': self.validate_by_id,
            'validate_by_aid': self.validate_by_aid,
            'validate_by_class': self.validate_by_class,
            'extract_by_jsonpath': self.extract_by_jsonpath,
            'extract_by_css': self.extract_by_css,
            'extract_by_xpath': self.extract_by_xpath,
            'extract_by_id': self.extract_by_id,
            'extract_by_aid': self.extract_by_aid,
            'extract_by_class': self.extract_by_class,
            'extract_by_eval': self.extract_by_eval,
        }
        self.add_actions(actions)

        # 延迟初始化driver
        self.driver = None
        # 当前页面的校验器, 依赖于driver
        self.validator = None
        # 当前页面的提取器, 依赖于driver
        self.extractor = None
        # 延迟初始化的app包
        self.package = None
        # 已下载过的url对应的文件，key是url，value是文件
        self.downloaded_files = {}
        # 基础url
        self._base_url = None
        # 是否在录屏
        self.recording = False

    # 执行多个步骤: 重写以便异常时结束录屏
    def run_steps(self, steps):
        try:
            # 逐个步骤调用多个动作
            i = 0
            for step in steps:
                for action, param in step.items():
                    self.run_action(action, param)
                    i += 1
        except Exception as ex:
            # 异常(忽略跳出循环的异常) + 正在录屏, 则结束录屏
            if (not isinstance(ex, BreakException)) and self.recording:
                self.try_stop_recording_screen(steps, i)
            raise ex

    # 调用后续的第一个停止录屏动作
    def try_stop_recording_screen(self, steps, start):
        # 逐个步骤检查多个动作
        i = 0
        for step in steps:
            for action, param in step.items():
                if i > start and action == 'stop_recording_screen':
                    log.error('Exception occur, stop recording screen')
                    # 调用动作
                    # self.run_action(action, param)
                    self.stop_recording_screen(param)
                    return

                i += 1

    # --------- 动作处理的函数 --------
    # 初始化driver
    def init_driver(self, config):
        '''
        # demo
        config = {
            'executor':'http://localhost:4723/wd/hub',
            'desired_caps': {
                "platformName": "Android",
                "platformVersion": "9",
                "deviceName": "f978cc97",
                "appPackage": "io.material.catalog",
                "appActivity": "io.material.catalog.main.MainActivity",
                "automationName": "UiAutomator2"
            }
        }
        '''
        # 替换配置中的变量
        config = replace_var(config, False)
        if 'executor' in config:
            executor = config['executor']
        else:
            executor = 'http://localhost:4723/wd/hub'
        if 'desired_caps' not in config:
            raise Exception(f'Miss driver desired_caps parameter')
        desired_caps = config['desired_caps']
        if 'appPackage' in desired_caps:
            package = desired_caps['appPackage']
        # 记录ios/android平台
        self.platform = desired_caps['platformName'].lower()
        # driver
        self.driver = webdriver.Remote(executor, desired_caps)
        # 当前页面的校验器, 依赖于driver
        self.validator = Validator(self.driver)
        # 当前页面的提取器, 依赖于driver
        self.extractor = Extractor(self.driver)

    # 关闭driver
    def close_driver(self):
        if self.driver != None:
            self.driver.quit()
            self.driver = None
            self.package = None

    @property
    def is_android(self):
        return self.platform == 'android'

    @property
    def is_ios(self):
        return self.platform == 'ios'

    # 检查并继续for循环
    def moveon_if_exist_by(self, config):
        self.break_if_not_exist_by(config)

    # 跳出for循环
    def break_if_not_exist_by(self, config):
        if not self.exist_by_any(config):
            raise BreakException(config)

    # 跳出for循环
    def break_if_exist_by(self, config):
        if self.exist_by_any(config):
            raise BreakException(config)

    # 解析响应
    def _analyze_response(self, res, config):
        # 添加固定变量:响应
        set_var('response', res)
        # 校验器
        v = Validator(self.driver, res)
        v.run(config)
        # 提取器
        e = Extractor(self.driver, res)
        e.run(config)

    # 根据组件id来填充输入框
    # :param input_data 表单数据, key是输入框的组件类名, value是填入的值
    def input_by_id(self, input_data):
        return self._input_by_type_and_data('id', input_data)

    # 根据组件aid来填充输入框
    # :param input_data 表单数据, key是输入框的组件类名, value是填入的值
    def input_by_aid(self, input_data):
        return self._input_by_type_and_data('aid', input_data)

    # 根据组件类名来填充输入框
    # :param input_data 表单数据, key是输入框的组件类名, value是填入的值
    def input_by_class(self, input_data):
        return self._input_by_type_and_data('class', input_data)

    # 根据xpath来填充输入框
    # :param input_data 表单数据, key是输入框的路径, value是填入的值
    def input_by_xpath(self, input_data):
        return self._input_by_type_and_data('xpath', input_data)

    # 根据类型与数据来填充输入框
    # :param type 选择器的类型:name/css/xpath
    # :param input_data 表单数据, key是输入框的路径, value是填入的值
    def _input_by_type_and_data(self, type, input_data):
        for name, value in input_data.items():
            value = replace_var(value)  # 替换变量

            # 找到输入框
            try:
                ele = self.find_by(type, name)
            except Exception as ex:  # 找不到元素
                log.error(f"Input element not found{name}", exc_info = ex)
                continue

            # ele.set_value(value)
            ele.clear() # 先清空
            ele.send_keys(value) # 后输入

    # 隐藏键盘
    def hide_keyboard(self, _):
        self.driver.hide_keyboard()

    # 根据指定类型，查找元素
    def find_by(self, type, path):
        return self.driver.find_element(type2by(type), path)

    # 根据任一类型，查找元素
    def find_by_any(self, config):
        types = ['id', 'aid', 'class', 'xpath']
        for type in types:
            if type in config:
                path = config[type]
                if type == 'xpath': # xpath支持变量
                    path = replace_var(path)
                return self.driver.find_element(type2by(type), path)
        raise Exception(f"Invalid find type: {config}")

    # 根据任一类型，查找元素
    def find_all_by_any(self, config):
        types = ['id', 'aid', 'class', 'xpath']
        for type in types:
            if type in config:
                path = config[type]
                return self.driver.find_elements(type2by(type), path)
        raise Exception(f"Invalid find type: {config}")

    # 根据指定类型，检查元素是否存在
    def exist_by(self, type, path):
        try:
            self.find_by(type, path)
            return True
        except NoSuchElementException:
            return False

    # 根据任一类型，检查元素是否存在
    def exist_by_any(self, config):
        try:
            self.find_by_any(config)
            return True
        except NoSuchElementException:
            return False

    # 屏幕滑动(传坐标), 无duration
    # :param config {from, to}
    def flick(self, config):
        x1, y1 = config['from'].split(",", 1) # 起点位置
        x2, y2 = config['to'].split(",", 1) # 终点位置
        self.driver.flick(x1, y1, x2, y2)

    # 屏幕横扫(传坐标), 有duration -- 多次调用多次滑,就算参数一样
    # :param config {from, to, duration}
    def swipe(self, config):
        x1, y1 = config['from'].split(",", 1) # 起点位置
        x2, y2 = config['to'].split(",", 1) # 终点位置
        duration = 0
        if 'duration' in config:
            duration = float(config['duration']) * 1000
        self.driver.swipe(x1, y1, x2, y2, duration)

    # 上滑(传比例) -- 多次调用多次滑,就算参数一样
    # :param 移动幅度比例
    def swipe_up(self, move_ratio):
        if move_ratio == None:
            move_ratio = 0.5
        end = (1 - move_ratio) / 2
        start = 1 - end
        # self.swipe_vertical(f'0.75,0.25')
        self.swipe_vertical(f'{start},{end}')

    # 下滑(传比例) -- 多次调用多次滑,就算参数一样
    # :param 移动幅度比例
    def swipe_down(self, move_ratio):
        if move_ratio == None:
            move_ratio = 0.5
        start = (1 - move_ratio) / 2
        end = 1 - start
        # self.swipe_vertical('0.25,0.75')
        self.swipe_vertical(f'{start},{end}')

    # 左滑(传y坐标) -- 多次调用多次滑,就算参数一样
    # :param y y坐标，固定不变，默认为中间
    def swipe_left(self, y = None):
        self.swipe_horizontal('0.75,0.25', y)

    # 右滑(传y坐标) -- 多次调用多次滑,就算参数一样
    # :param y y坐标，固定不变，默认为中间
    def swipe_right(self, y = None):
        self.swipe_horizontal('0.25,0.75', y)

    # 垂直方向(上下)滑动 -- 多次调用多次滑,就算参数一样
    # :param y_range_ratios y轴起点/终点位置在屏幕的比例，如 0.2,0.7，即y轴上从屏幕0.2比例处滑到0.7比例处
    # :param xm x坐标，固定不变，默认为中间
    def swipe_vertical(self, y_range_ratios, xm = None):
        # 获取屏幕的宽高
        size = self.driver.get_window_size()
        w = size["width"]
        h = size["height"]
        # x不变：水平居中
        if xm == None:
            xm = int(w * 0.5)
        # y:按比例计算坐标
        y1_ratio, y2_ratio = y_range_ratios.split(",", 1) # y轴起点/终点位置在屏幕的比例
        y1 = int(h * float(y1_ratio))
        y2 = int(h * float(y2_ratio))
        duration = 0.1 * 1000
        log.info(f"xm={xm}, y1={y1}, xm={xm}, y2={y2}, ")
        self.driver.swipe(xm, y1, xm, y2, duration)

    # 水平方向(左右)滑动 -- 多次调用多次滑,就算参数一样
    # :param x_range_ratios x轴起点/终点位置在屏幕的比例，如 0.2,0.7，即x轴上从屏幕0.2比例处滑到0.7比例处
    # :param ym y坐标，固定不变，默认为中间
    def swipe_horizontal(self, x_range_ratios, ym = None):
        # 获取屏幕的宽高
        size = self.driver.get_window_size()
        w = size["width"]
        h = size["height"]
        # y不变：水平居中
        if ym == None:
            ym = int(h * 0.5)
        # x:按比例计算坐标
        x1_ratio, x2_ratio = x_range_ratios.split(",", 1)  # x轴起点/终点位置在屏幕的比例
        x1 = int(w * float(x1_ratio))
        x2 = int(w * float(x2_ratio))
        duration = 0.1 * 1000
        self.driver.swipe(x1, ym, x2, ym, duration)

    # 向下滚, 仅ios有效
    def scroll_down_by(self, config):
        ele = self.find_by_any(config)
        self.driver.execute_script("mobile: scroll", {"direction": 'down', 'elementid': ele.id})

    # 向上滚, 仅ios有效
    def scroll_up_by(self, config):
        ele = self.find_by_any(config)
        self.driver.execute_script("mobile: scroll", {"direction": 'up', 'elementid': ele.id})

    # 移动轨迹(传坐标序列)
    # :param positions 坐标序列 如x1,y1;x2,y2
    def move_track(self, positions):
        positions = positions.split(";")
        '''TouchAction已失效, 没有产生动作: 报错[Deprecated] 'TouchAction' action is deprecated. Please use W3C actions instead.
        # TouchAction(self.driver).press(None, x1, y1).move_to(None, x2, y2).release().perform()
        action = TouchAction(self.driver)
        for i in range(0, len(positions)):
            x, y = positions[i].split(",", 1)  # 坐标
            if i == 0:
                action.press(None, x, y)
            else:
                action.move_to(None, x, y)
        action.release().perform()
        '''
        actions = ActionChains(self.driver)
        actions.w3c_actions.devices = []
        finger = actions.w3c_actions.add_pointer_input('touch', 'finger')
        for i in range(0, len(positions)):
            x, y = positions[i].split(",", 1)  # 坐标
            # 手指移动
            finger.create_pointer_move(x=x, y=y)
            if i == 0: # 开始:手指按下去
                finger.create_pointer_down(button=MouseButton.LEFT)

        # 最后:手指松开
        finger.create_pointer_up(MouseButton.LEFT)
        actions.perform()

    # 拖拽(传元素): 从一个元素滑动到另一个元素，第二个元素替代第一个元素原本屏幕上的位置
    # :param config {by, from, to}
    def drag_and_drop_by(self, config):
        by = config['by']
        _from = self.find_by(by, config['from']) # 起点元素
        to = self.find_by(by, config['to']) # 终点元素
        self.driver.drag_and_drop(_from, to)

    # 滚动(传元素): 从一个元素滚动到另一元素，直到页面自动停止(有惯性)
    # :param config {by, from, to, duration}
    def scroll_by(self, config):
        by = config['by']
        _from = self.find_by(by, config['from']) # 起点元素
        to = self.find_by(by, config['to']) # 终点元素
        duration = None
        if 'duration' in config:
            duration = float(config['duration']) * 1000
        self.driver.scroll(_from, to, duration)

    # 移动(传元素): 从一个元素移动到另一元素，无惯性
    # :param config {by, from, to, duration}
    def move_by(self, config):
        by = config['by']
        _from = self.find_by(by, config['from']).location # 起点元素的位置
        to = self.find_by(by, config['to']).location # 终点元素的位置
        duration = None
        if 'duration' in config:
            duration = float(config['duration'])

        actions = ActionChains(self.driver)
        actions.w3c_actions.devices = []
        finger = actions.w3c_actions.add_pointer_input('touch', 'finger')
        # 手指移动到开头
        finger.create_pointer_move(x=_from['x'], y=_from['y'])
        # 开始:手指按下去
        finger.create_pointer_down(button=MouseButton.LEFT)
        # 手指移动到结尾
        finger.create_pointer_move(x=to['x'], y=to['y'])
        # 最后:手指松开
        finger.create_pointer_up(MouseButton.LEFT)
        actions.perform()

    # 放大
    def zoom_in(self, _):
        self.do_zoom(True)

    # 缩小
    def zoom_out(self, _):
        self.do_zoom(False)

    # 真正的缩放
    def do_zoom(self, is_up):
        actions = ActionChains(self.driver)
        actions.w3c_actions.devices = []
        finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
        finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        # 两个手指移动到开始
        xm = width * 0.5
        start1, start2, end1, end2 = self.get_zoom_y_range_ratios(is_up)
        finger1.create_pointer_move(x=xm, y=height * start1)
        finger2.create_pointer_move(x=xm, y=height * start2)
        # 两个手指按下去
        finger1.create_pointer_down(button=MouseButton.LEFT)
        finger2.create_pointer_down(button=MouseButton.LEFT)
        # 两个手指移动到结尾
        finger1.create_pointer_move(x=xm, y=height * end1)
        finger2.create_pointer_move(x=xm, y=height * end2)
        # 两个手指松开
        finger1.create_pointer_up(MouseButton.LEFT)
        finger2.create_pointer_up(MouseButton.LEFT)
        actions.perform()

    # 获得缩放时2个手指的y轴起点/终点位置在屏幕的比例，分别是: 两个手指的起点y比例, 两个手指的终点y比例
    def get_zoom_y_range_ratios(self, is_up):
        if is_up: # 放大：从中间到两边
            return 0.5, 0.5, 9.9, 0.1

        # 缩小: 从两边到中间
        return 9.9, 0.1, 0.5, 0.5

    # 通过坐标方式敲击屏幕
    # :param config {positions, duration} 或 positions, 其中 positions 为坐标序列 如x1,y1;x2,y2; 而 duration 可以模拟长按
    def tap(self, config):
        # TouchAction过时
        # x, y = pos.split(",", 1)
        # TouchAction(self.driver).tap(None, x, y).perform()

        duration = None
        if isinstance(config, dict):
            positions = config['positions']
            if 'duration' in config:
                duration = float(config['duration']) * 1000
        else:
            positions = config

        # 坐标序列(如x1,y1;x2,y2) 转 List[Tuple[int, int]]
        positions = list(map(lambda pos: tuple(pos.split(",", 1)), positions.split(";")))
        self.driver.tap(positions, duration)

    # 敲击屏幕
    # :param config {id, aid, class, xpath}
    def tap_by(self, config):
        ele = self.find_by_any(config)
        # TouchAction过时
        #TouchAction(self.driver).tap(ele).perform()

        loc = ele.location
        size = ele.size
        # 取元素中心位置
        x = loc['x'] + size['width'] / 2
        y = loc['y'] + size['height'] / 2

        duration = None
        if 'duration' in config:
            duration = float(config['duration']) * 1000

        self.driver.tap([(x,y)], duration)

    # 点击按钮
    # :param config {id, aid, class, xpath}
    def click_by(self, config):
        ele = self.find_by_any(config)
        ele.click()

    # 如果按钮存在，则点击
    # :param config {id, aid, class, xpath}
    def click_by_if_exist(self, config):
        try:
            ele = self.find_by_any(config)
        except:
            ele = None
        if ele != None:
            ele.click()

    # 摇一摇
    def shake(self, _):
        self.driver.shake()

    # 旋转
    # :param is_portrait 是否竖屏
    def set_orientation(self, is_portrait):
        '''
        PORTRAIT 竖屏模式
        LANDSCAPE 宽屏模式
        '''
        if self.driver.orientation == 'PORTRAIT':
            target = 'LANDSCAPE'
        else:
            target = 'PORTRAIT'
        self.driver.orientation = target

    # 设置地理位置
    # :param loc 地理位置,格式为`纬度,经度,海拔高度`
    def set_location(self, loc):
        parts = loc.split(",", 2)
        lat = parts[0]  # 纬度
        lon = parts[1]  # 经度
        if len(parts) > 2:
            alt = parts[2]  # 海拔高度
        else:
            alt = None
        self.driver.set_location(lat, lon, alt)

    # 整个窗口截图存为png
    # :param config {save_dir, save_file}
    def screenshot(self, config):
        # 文件名
        default_file = str(time.time()).split(".")[0] + ".png"
        save_file = self._prepare_save_file(config, default_file)
        self.driver.save_screenshot(save_file)

    # 对某个标签截图存为png
    # :param config {id, class, xpath, save_dir, save_file}
    def screenshot_element_by(self, config):
        ele = self.find_by_any(config)
        # 文件名
        default_file = str(time.time()).split(".")[0] + ".png" # 默认文件名
        save_file = self._prepare_save_file(config, default_file)
        ele.screenshot(save_file)

    # 执行js
    def execute_js(self, js):
        self.driver.execute_script(js)

    # 返回键
    def back(self, _):
        self.keyevent(4)

    # 回车
    def enter(self, _):
        self.keyevent(66)

    # 模拟系统键
    def keyevent(self, code):
        self.driver.keyevent(code)
        # self.driver.press_keycode(code)

    # 打开手机的通知栏
    def open_notifications(self):
        self.driver.open_notifications()

    # 读剪切板
    # :param var 记录剪切板内容的变量名
    def get_clipboard(self, var_name):
        set_var(var_name, self.driver.get_clipboard())

    # 写剪切板
    # :param txt 写入内容
    def set_clipboard(self, txt):
        txt = replace_var(txt)
        self.driver.set_clipboard(txt)

    # 推文件到手机上, 即写手机上文件
    # :param config {to,content,from} content与from是二选一
    def push_file(self, config):
        to = replace_var(config['to'])
        # 写入内容
        if 'content' in config:
            content = replace_var(config['content'])
        elif 'from' in config:
            _from = replace_var(config['from'])
            content = read_file(_from)
        else:
            raise Exception('Miss content or from parameter, cannot get push content')
        # 转base64
        data = bytes(content, 'utf-8')
        data = base64.b64encode(data).decode('utf-8')
        # 写文件
        self.driver.push_file(to, data)

    # 从手机中拉文件, 即读手机上的文件
    # :param config {from,var,to}
    def pull_file(self, config):
        _from = replace_var(config['from'])
        # 读文件
        file_base64 = self.driver.pull_file(_from)
        # base64解码
        file_content = base64.b64decode(file_base64).decode('utf-8')
        # 写变量
        if 'var' in config:
            set_var(config['var'], file_content)
        # 写文件
        if 'to' in config:
            to = replace_var(config['to'])
            write_file(to, file_content)

    # 发送短信
    def send_sms(self, config):
        phone = replace_var(config['phone'])
        content = replace_var(config['content'])
        self.driver.send_sms(phone, content)

    # 打印性能信息
    def print_performance(self, _):
        types = self.driver.get_performance_data_types()
        perfs = {}
        for type in types:
            perfs[type] = self.driver.get_performance_data(self.package, type)
        log.info(perfs)

    # 开始录屏
    def start_recording_screen(self, _):
        self.recording = True
        self.driver.start_recording_screen()

    # 停止录屏
    def stop_recording_screen(self, path):
        self.recording = False
        # 1 有remotePath是上传的地址，只支持 http/https 与 ftp/ftps 协议
        #self.driver.stop_recording_screen(remotePath = 'http://xxx/yyy.mp4', user = '', password='', method='post')

        # 2 无remotePath, 直接返回视频数据的base64编码
        data = self.driver.stop_recording_screen()
        # base64解码
        data = base64.b64decode(data)
        # 存为mp4文件
        if path == None:
            path = time.strftime('record-%Y%m%d-%H%M%S') + '.mp4'
        path = self._prepare_save_file({}, path)
        write_byte_file(path, data)

    # 点击弹框的确定按钮, 如授权弹框的允许
    def alert_accept(self, _):
        src = self.driver.page_source
        if '允许' in src or 'allow' in src:
            self.driver.switch_to.alert.accept()

    # 取消弹框, 如授权弹窗的禁止
    def alert_dismiss(self, _):
        src = self.driver.page_source
        if '允许' in src or 'allow' in src:
            self.driver.switch_to.alert.dismiss()

    # 设置基础url
    def base_url(self, url):
        self._base_url = url

    # 拼接url
    def _get_url(self, config):
        url = config['url']
        url = replace_var(url)  # 替换变量
        # 添加基url
        if (self._base_url is not None) and ("http" not in url):
            url = self._base_url + url
        return url

    # get请求
    # :param config {url, is_ajax, data, validate_by_jsonpath, validate_by_css, validate_by_xpath, extract_by_jsonpath, extract_by_css, extract_by_xpath, extract_by_eval}
    def get(self, config = {}):
        url = self._get_url(config)
        data = replace_var(config['data'], False)
        headers = {}
        if 'is_ajax' in config and config['is_ajax']:
            headers = {
                'X-Requested-With': 'XMLHttpRequest'
            }
        res = requests.get(url, headers=headers, data=data)
        # log.debug(res.text)
        # 解析响应
        self._analyze_response(res, config)

    # post请求
    # :param config {url, is_ajax, data, validate_by_jsonpath, validate_by_css, validate_by_xpath, extract_by_jsonpath, extract_by_css, extract_by_xpath, extract_by_eval}
    def post(self, config = {}):
        url = self._get_url(config)
        data = replace_var(config['data'], False)
        headers = {}
        if 'is_ajax' in config and config['is_ajax']:
            headers = {
                'X-Requested-With': 'XMLHttpRequest'
            }
        res = requests.post(url, headers=headers, data=data)
        # 解析响应
        self._analyze_response(res, config)

    # 上传文件
    # :param config {url, files, validate_by_jsonpath, validate_by_css, validate_by_xpath, extract_by_jsonpath, extract_by_css, extract_by_xpath, extract_by_eval}
    def upload(self, config = {}):
        url = self._get_url(config)
        # 文件
        files = {}
        for name, path in config['files'].items():
            path = replace_var(path)
            files[name] = open(path, 'rb')
        # 发请求
        res = requests.post(url, files=files)
        # 解析响应
        self._analyze_response(res, config)

    # 下载文件
    # :param config {url, save_dir, save_file}
    def download(self, config={}):
        url = self._get_url(config)
        # 文件名
        save_file = self._prepare_save_file(config, url)
        # 真正的下载
        self._do_download(url, save_file)
        return save_file

    # 获得文件名
    # config['save_dir'] + config['save_file'] 或 url中的默认文件名
    def _prepare_save_file(self, config, url):
        # 获得保存的目录
        if 'save_dir' in config:
            save_dir = config['save_dir']
        else:
            save_dir = 'downloads'
        # 获得保存的文件名
        if 'save_file' in config:
            save_file = config['save_file']
        else:
            save_file = os.path.basename(url)
        save_file = os.path.abspath(save_dir + os.sep + save_file)  # 转绝对路径
        # 准备目录
        dir, name = os.path.split(save_file)
        if not os.path.exists(dir):
            os.makedirs(dir)
        # 检查重复
        if os.path.exists(save_file):
            for i in range(100000000000000):
                if '.' in save_file:
                    path, ext = save_file.rsplit(".", 1) # 从后面分割，分割为路径+扩展名
                    newname = f"{path}-{i}.{ext}"
                else:
                    newname = f"{save_file}-{i}"
                if not os.path.exists(newname):
                    return newname
            raise Exception('Too many file in save_dir, please change other directory.')

        return save_file

    # 执行下载文件
    def _do_download(self, url, save_file):
        if url in self.downloaded_files:
            return self.downloaded_files[url]

        # 发请求
        res = requests.get(url)
        # 保存响应的文件
        write_byte_file(save_file, res.content)
        # 设置变量
        set_var('download_file', save_file)
        self.downloaded_files[url] = save_file
        log.debug(f"Dowload file: url is {url}, save path is{save_file}")
        return save_file

    # 识别url中的验证码
    def recognize_captcha(self, config={}):
        # 下载图片
        file = self.download(config)
        # 识别验证码
        self._do_recognize_captcha(file)

    # 识别验证码标签中的验证码
    def recognize_captcha_element(self, config={}):
        # 下载图片
        file_path = self.screenshot_element_by(config)
        # 识别验证码
        self._do_recognize_captcha(file_path)

    # 真正的识别验证码
    def _do_recognize_captcha(self, file_path):
        # 1 使用 pytesseract 识别图片 -- wrong: 默认没训练过的识别不了
        # img = Image.open(file_path)
        # captcha = pytesseract.image_to_string(img)
        # 2 使用有道ocr
        captcha = ocr_youdao.recognize_text(file_path)
        # 设置变量
        set_var('captcha', captcha)
        log.debug(f"Recognize captcha: image file is {file_path}, captcha is {captcha}")
        # 删除文件
        #os.remove(file)

    def validate_by_jsonpath(self, fields):
        return self.validator.run_type('jsonpath', fields)

    def validate_by_css(self, fields):
        return self.validator.run_type('css', fields)

    def validate_by_xpath(self, fields):
        return self.validator.run_type('xpath', fields)

    def validate_by_id(self, fields):
        return self.validator.run_type('id', fields)

    def validate_by_aid(self, fields):
        return self.validator.run_type('aid', fields)

    def validate_by_class(self, fields):
        return self.validator.run_type('class', fields)

    def extract_by_jsonpath(self, fields):
        return self.extractor.run_type('jsonpath', fields)

    def extract_by_css(self, fields):
        return self.extractor.run_type('css', fields)

    def extract_by_xpath(self, fields):
        return self.extractor.run_type('xpath', fields)

    def extract_by_id(self, fields):
        return self.extractor.run_type('id', fields)

    def extract_by_aid(self, fields):
        return self.extractor.run_type('aid', fields)

    def extract_by_class(self, fields):
        return self.extractor.run_type('class', fields)

    def extract_by_eval(self, fields):
        return self.extractor.run_eval(fields)

# cli入口
def main():
    # 基于yaml的执行器
    boot = Boot()
    # 读元数据：author/version/description
    dir = os.path.dirname(__file__)
    meta = read_init_file_meta(dir + os.sep + '__init__.py')
    # 步骤配置的yaml
    step_files, option = parse_cmd('AppiumBoot', meta['version'])
    if len(step_files) == 0:
        raise Exception("Miss step config file or directory")
    try:
        # 执行yaml配置的步骤
        boot.run(step_files)
    except Exception as ex:
        activity = ''
        src = ''
        if boot.driver != None:
            activity = boot.driver.current_activity
            src = boot.driver.page_source
            # report_to_sauce(boot.driver.session_id)
            # take_screenshot_and_logcat(boot.driver, device_logger, calling_request)
        # log.error(f"Exception occurs: current step file is {step_file}, current activity is {activity}, current page source is {src}", exc_info = ex)
        log.error(f"Exception occurs: current step file is {boot.step_file}, current activity is {activity}", exc_info = ex)
        raise ex
    finally:
        boot.close_driver()

if __name__ == '__main__':
    main()