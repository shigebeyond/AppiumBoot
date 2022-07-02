#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import sys
import os
import fnmatch
from pathlib import Path
from ocr import *
from util import *
import ast
import util
import validator
import extractor
from helpers import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.action_chains import ActionChains

from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 跳出循环的异常
class BreakException(Exception):
    def __init__(self, condition):
        self.condition = condition # 跳转条件

# appium基于yaml的启动器
class Boot(object):

    def __init__(self):
        # 延迟初始化driver
        self.driver = None
        # 步骤文件所在的目录
        self.step_dir = None
        # 已下载过的url对应的文件，key是url，value是文件
        self.downloaded_files = {}
        # 基础url
        self.base_url = None
        # 动作映射函数
        self.actions = {
            'init_driver': self.init_driver,
            'close_driver': self.close_driver,
            'sleep': self.sleep,
            'print': self.print,
            'get': self.get,
            'post': self.post,
            'upload': self.upload,
            'download': self.download,
            'recognize_captcha': self.recognize_captcha,
            'recognize_captcha_element': self.recognize_captcha_element,
            'input_by_id': self.input_by_id,
            'input_by_class': self.input_by_class,
            'input_by_xpath': self.input_by_xpath,
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
            'long_press': self.long_press,
            'long_press_by': self.long_press_by,
            'click_by': self.click_by,
            'double_click_by': self.double_click_by,
            'screenshot': self.screenshot,
            'screenshot_element_by': self.screenshot_element_by,
            'execute_js': self.execute_js,
            'back': self.back,
            'keyevent': self.keyevent,
            'open_notifications': self.open_notifications,
            'for': self.do_for,
            'once': self.once,
            'break_if': self.break_if,
            'moveon_if': self.moveon_if,
            'include': self.include,
            'set_vars': self.set_vars,
            'print_vars': self.print_vars,
        }

    '''
    执行入口
    :param step_files 步骤配置文件或目录的列表
    '''
    def run(self, step_files):
        for path in step_files:
            # 1 模式文件
            if '*' in path:
                dir, pattern = path.rsplit(os.sep, 1)  # 从后面分割，分割为目录+模式
                if not os.path.exists(dir):
                    raise Exception(f'步骤配置目录不存在: {dir}')
                self.run_1dir(dir, pattern)
                return

            # 2 不存在
            if not os.path.exists(path):
                raise Exception(f'步骤配置文件或目录不存在: {path}')

            # 3 目录: 遍历执行子文件
            if os.path.isdir(path):
                self.run_1dir(path)
                return

            # 4 纯文件
            self.run_1file(path)

    # 执行单个步骤目录: 遍历执行子文件
    # :param path 目录
    # :param pattern 文件名模式
    def run_1dir(self, dir, pattern ='*.yml'):
        # 遍历目录: https://blog.csdn.net/allway2/article/details/124176562
        files = os.listdir(dir)
        files.sort() # 按文件名排序
        for file in files:
            if fnmatch.fnmatch(file, pattern): # 匹配文件名模式
                file = os.path.join(dir, file)
                if os.path.isfile(file):
                    self.run_1file(file)

    # 执行单个步骤文件
    # :param step_file 步骤配置文件路径
    # :param include 是否inlude动作触发
    def run_1file(self, step_file, include = False):
        # 获得步骤文件的绝对路径
        if include: # 补上绝对路径
            if not os.path.isabs(step_file):
                step_file = self.step_dir + os.sep + step_file
        else: # 记录目录
            step_file = os.path.abspath(step_file)
            self.step_dir = os.path.dirname(step_file)

        print(f"加载并执行步骤文件: {step_file}")
        # 获得步骤
        steps = read_yaml(step_file)
        try:
            # 执行多个步骤
            self.run_steps(steps)
        except Exception as ex:
            activity = ''
            if self.driver != None:
                activity = self.driver.current_activity
                # report_to_sauce(self.driver.session_id)
                # take_screenshot_and_logcat(self.driver, device_logger, calling_request)
            print(f"异常环境:当前步骤文件为 {step_file}, 当前activity为 {activity}")
            raise ex

    # 执行多个步骤
    def run_steps(self, steps):
        # 逐个步骤调用多个动作
        for step in steps:
            for action, param in step.items():
                self.run_action(action, param)

    '''
    执行单个动作：就是调用动作名对应的函数
    :param action 动作名
    :param param 参数
    '''
    def run_action(self, action, param):
        if 'for(' in action:
            n = int(action[4:-1])
            self.do_for(param, n)
            return

        if action not in self.actions:
            raise Exception(f'无效动作: [{action}]')

        # 调用动作对应的函数
        print(f"处理动作: {action}={param}")
        func = self.actions[action]
        func(param)

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
        if 'executor' in config:
            executor = config['executor']
        else:
            executor = 'http://localhost:4723/wd/hub'
        if 'desired_caps' not in config:
            raise Exception(f'未指定driver的desired_caps参数')
        self.driver = webdriver.Remote(executor, config['desired_caps'])

    # 关闭driver
    def close_driver(self):
        if self.driver != None:
            self.driver.quit()
            self.driver = None

    # for循环
    # :param steps 每个迭代中要执行的步骤
    # :param n 循环次数
    def do_for(self, steps, n = None):
        label = f"for({n})"
        if n == None:
            n = sys.maxsize # 最大int，等于无限循环次数
            label = f"for(∞)"
        print(f"-- 开始循环: {label} -- ")
        try:
            for i in range(n):
                # i+1表示迭代次数比较容易理解
                print(f"第{i+1}次迭代")
                set_var('for_i', i+1)
                self.run_steps(steps)
        except BreakException as e:  # 跳出循环
            print(f"-- 跳出循环: {label}, 跳出条件: {e.condition} -- ")
        else:
            print(f"-- 结束循环: {label} -- ")

    # 执行一次子步骤，相当于 for(1)
    def once(self, steps):
        self.do_for(steps, 1)

    # 检查并继续for循环
    def moveon_if(self, expr):
        # break_if(条件取反)
        self.break_if(f"not ({expr})")

    # 跳出for循环
    def break_if(self, expr):
        val = eval(expr, globals(), util.vars)  # 丢失本地与全局变量, 如引用不了json模块
        if bool(val):
            raise BreakException(expr)

    # 加载并执行其他步骤文件
    def include(self, step_file):
        self.run_1file(step_file, True)

    # 设置变量
    def set_vars(self, vars):
        for k, v in vars.items():
            v = replace_var(v)  # 替换变量
            set_var(k, v)

    # 打印变量
    def print_vars(self, _):
        print(f"打印变量: {util.vars}")

    # 睡眠
    def sleep(self, seconds):
        time.sleep(seconds)

    # 打印
    def print(self, msg):
        msg = replace_var(msg)  # 替换变量
        print(msg)

    # 解析响应
    def _analyze_response(self, res, config):
        # 添加固定变量:响应
        set_var('response', res)
        # 校验器
        v = validator.Validator(self.driver, res)
        v.run(config)
        # 提取器
        e = extractor.Extractor(self.driver, res)
        e.run(config)

    # 设置基础url
    def set_base_url(self, url):
        self.base_url = url

    # 拼接url
    def _get_url(self, config):
        url = config['url']
        url = replace_var(url)  # 替换变量
        # 添加基url
        if (self.base_url is not None) and ("http" not in url):
            url = self.base_url + url
        return url

    # get请求
    # :param config {url, is_ajax, validate_by_jsonpath, validate_by_class, validate_by_xpath, extract_by_jsonpath, extract_by_class, extract_by_xpath, extract_by_eval}
    def get(self, config = {}):
        url = self._get_url(config)
        headers = {}
        if 'is_ajax' in config and config['is_ajax']:
            headers = {
                'X-Requested-With': 'XMLHttpRequest'
            }
        res = self.driver.request('GET', url, headers=headers)
        # print(res.text)
        # 解析响应
        self._analyze_response(res, config)

    # post请求
    # :param config {url, is_ajax, data, validate_by_jsonpath, validate_by_class, validate_by_xpath, extract_by_jsonpath, extract_by_class, extract_by_xpath, extract_by_eval}
    def post(self, config = {}):
        url = self._get_url(config)
        data = replace_var(config['data'])
        headers = {}
        if 'is_ajax' in config and config['is_ajax']:
            headers = {
                'X-Requested-With': 'XMLHttpRequest'
            }
        res = self.driver.request('POST', url, headers=headers, data=data)
        # 解析响应
        self._analyze_response(res, config)

    # 上传文件
    # :param config {url, files, validate_by_jsonpath, validate_by_class, validate_by_xpath, extract_by_jsonpath, extract_by_class, extract_by_xpath, extract_by_eval}
    def upload(self, config = {}):
        url = self._get_url(config)
        # 文件
        files = {}
        for name, path in config['files'].items():
            path = replace_var(path)
            files[name] = open(path, 'rb')
        # 发请求
        res = self.driver.request('POST', url, files=files)
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
            raise Exception('目录太多文件，建议新建目录')

        return save_file

    # 执行下载文件
    def _do_download(self, url, save_file):
        if url in self.downloaded_files:
            return self.downloaded_files[url]

        # 发请求
        res = self.driver.request('GET', url)
        # 保存响应的文件
        file = open(save_file, 'wb')
        file.write(res.content)
        file.close()
        # 设置变量
        set_var('download_file', save_file)
        self.downloaded_files[url] = save_file
        print(f"下载文件: url为{url}, 另存为{save_file}")
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
        print(f"识别验证码: 图片为{file_path}, 验证码为{captcha}")
        # 删除文件
        #os.remove(file)

    # 根据组件id来填充输入框
    # :param input_data 表单数据, key是输入框的组件类名, value是填入的值
    def input_by_id(self, input_data):
        return self._input_by_type_and_data('id', input_data)

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
            print(f"替换变量： {name} = {value}")
            value = replace_var(value)  # 替换变量

            # 找到输入框
            try:
                ele = self._find_by(type, name)
            except Exception as ex:  # 找不到元素
                print_exception(f"找不到输入元素{name}")
                print_exception(str(ex))
                continue

            if ele.tag_name == 'select': # 设置输入框
                # js = f"$('select[name={name}]')[0].selectedIndex = '{value}'"
                # self.driver.execute_script(js)
                Select(ele).select_by_value(value)
            elif ele.get_attribute('type') == "hidden": # 设置隐藏域
                # hidden input调用send_keys()报错：selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
                # https://www.cnblogs.com/qican/p/14037564.html
                #js = f"$('input[name={name}]').val('{value}')" # jquery
                js = f"arguments[0].value = '{value}'" # 原生js
                self.driver.execute_script(js, ele)
            else:
                ele.clear() # 先清空
                ele.send_keys(value) # 后输入

    # 类型转by
    def type2by(self, type):
        if type == 'id':
            return By.ID
        if type == 'aid':
            return By.ACCESSIBILITY_ID
        if type == 'class':
            return By.CLASS_NAME
        if type == 'xpath':
            return By.XPATH
        raise Exception(f"不支持查找类型: {type}")

    # 根据指定类型，查找元素
    def _find_by(self, type, path):
        return self.driver.find_element(self.type2by(type), path)

    # 根据任一类型，查找元素
    def _find_by_any(self, config):
        types = ['id', 'aid', 'class', 'xpath']
        for type in types:
            if type in config:
                path = config[type]
                if type == 'xpath': # xpath支持变量
                    path = replace_var(path)
                return self.driver.find_element(self.type2by(type), path)
        raise Exception(f"没有查找类型: {config}")

    # 根据任一类型，查找元素
    def _find_all_by_any(self, config):
        types = ['id', 'aid', 'class', 'xpath']
        for type in types:
            if type in config:
                path = config[type]
                return self.driver.find_elements(self.type2by(type), path)
        raise Exception(f"没有查找类型: {config}")

    # 屏幕滑动(传坐标)
    # :param config {from, to, duration}
    def flick(self, config):
        x1, y1 = config['from'].split(",", 1) # 起始位置
        x2, y2 = config['to'].split(",", 1) # 结束位置
        duration = 0
        if 'duration' in config:
            duration = int(config['duration'])
        self.driver.flick(x1, y1, x2, y2, duration)

    # 屏幕横扫(传坐标)
    # :param config {from, to, duration}
    def swipe(self, config):
        x1, y1 = config['from'].split(",", 1) # 起始位置
        x2, y2 = config['to'].split(",", 1) # 结束位置
        duration = 0
        if 'duration' in config:
            duration = int(config['duration'])
        self.driver.swipe(x1, y1, x2, y2, duration)

    # 上滑
    # :param 移动幅度比例
    def swipe_up(self, move_ratio):
        if move_ratio == None:
            move_ratio = 0.5
        end = (1 - move_ratio) / 2
        start = 1 - end
        # self.swipe_vertical(f'0.75,0.25')
        self.swipe_vertical(f'{start},{end}')

    # 下滑
    def swipe_down(self, move_ratio):
        if move_ratio == None:
            move_ratio = 0.5
        start = (1 - move_ratio) / 2
        end = 1 - start
        # self.swipe_vertical('0.25,0.75')
        self.swipe_vertical(f'{start},{end}')

    # 左滑
    def swipe_left(self, _):
        self.swipe_horizontal('0.75,0.25')

    # 右滑
    def swipe_right(self, _):
        self.swipe_horizontal('0.25,0.75')

    # 垂直方向(上下)滑动
    # :param y_range_ratios y轴起始位置在屏幕的比例，如 0.2,0.7，即从屏幕0.2比例处滑到0.7比例处
    def swipe_vertical(self, y_range_ratios):
        # 获取屏幕的宽高
        size = self.driver.get_window_size()
        w = size["width"]
        h = size["height"]
        # x不变：水平居中
        xm = int(w * 0.5)
        # y:按比例计算坐标
        y1_ratio, y2_ratio = y_range_ratios.split(",", 1) # y轴起始位置在屏幕的比例
        y1 = int(h * float(y1_ratio))
        y2 = int(h * float(y2_ratio))
        duration = 1000
        self.driver.swipe(xm, y1, xm, y2, duration)

    # 水平方向(左右)滑动
    # :param x_range_ratios x轴起始位置在屏幕的比例，如 0.2,0.7，即从屏幕0.2比例处滑到0.7比例处
    def swipe_horizontal(self, x_range_ratios):
        # 获取屏幕的宽高
        size = self.driver.get_window_size()
        w = size["width"]
        h = size["height"]
        # y不变：水平居中
        ym = int(h * 0.5)
        # x:按比例计算坐标
        x1_ratio, x2_ratio = x_range_ratios.split(",", 1)  # x轴起始位置在屏幕的比例
        x1 = int(w * float(x1_ratio))
        x2 = int(w * float(x2_ratio))
        duration = 1000
        self.driver.swipe(x1, ym, x2, ym, duration)

    # 移动轨迹(传坐标数组)
    # :param pos_list
    def move_track(self, pos_list):
        '''TouchAction已失效, 没有产生动作: 报错[Deprecated] 'TouchAction' action is deprecated. Please use W3C actions instead.
        # TouchAction(self.driver).press(None, x1, y1).move_to(None, x2, y2).release().perform()
        action = TouchAction(self.driver)
        for i in range(0, len(pos_list)):
            x, y = pos_list[i].split(",", 1)  # 坐标
            if i == 0:
                action.press(None, x, y)
            else:
                action.move_to(None, x, y)
        action.release().perform()
        '''
        actions = ActionChains(self.driver)
        actions.w3c_actions.devices = []
        finger = actions.w3c_actions.add_pointer_input('touch', 'finger')
        for i in range(0, len(pos_list)):
            x, y = pos_list[i].split(",", 1)  # 坐标
            # 手指移动
            finger.create_pointer_move(x=x, y=y)
            if i == 0: # 开始:手指按下去
                finger.create_pointer_down(button=MouseButton.LEFT)

        # 最后:手指松开
        finger.create_pointer_up(MouseButton.LEFT)
        actions.perform()

    # 拖拽(传元素): 从一个元素滑动到另一个元素，第二个元素替代第一个元素原本屏幕上的位置
    # :param config {from, to}
    def drag_and_drop_by(self, config):
        by = config['by']
        _from = self._find_by(by, config['from']) # 起始元素
        to = self._find_by(by, config['to']) # 结束元素
        self.driver.drag_and_drop(_from, to)

    # 滑动(传元素): 从一个元素滑动到另一元素，直到页面自动停止(有惯性)
    # :param config {from, to, duration}
    def scroll_by(self, config):
        by = config['by']
        _from = self._find_by(by, config['from']) # 起始元素
        to = self._find_by(by, config['to']) # 结束元素
        duration = None
        if 'duration' in config:
            duration = int(config['duration'])
        self.driver.scroll(_from, to, duration)

    # 滑动(传元素): 从一个元素滑动到另一元素，无惯性
    # :param config {from, to, duration}
    def move_by(self, config):
        by = config['by']
        _from = self._find_by(by, config['from']).location # 起始元素的位置
        to = self._find_by(by, config['to']).location # 结束元素的位置
        duration = None
        if 'duration' in config:
            duration = int(config['duration'])
        # print(_from)
        # print(to)

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

    # 获得缩放时2个手指的y轴起始位置在屏幕的比例，分别是: 两个手指的起始y比例, 两个手指的结束y比例
    def get_zoom_y_range_ratios(self, is_up):
        if is_up: # 放大：从中间到两边
            return 0.5, 0.5, 9.9, 0.1

        # 缩小: 从两边到中间
        return 9.9, 0.1, 0.5, 0.5

    # 通过坐标方式敲击屏幕
    # :param pos x,y
    def tap(self, pos):
        x, y = pos.split(",", 1)
        # self.driver.tap([(x, y)]) # 一样的
        TouchAction(self.driver).tap(None, x, y).perform()

    # 敲击屏幕
    # :param config {id, class, xpath}
    def tap_by(self, config):
        ele = self._find_by_any(config)
        TouchAction(self.driver).tap(ele).perform()

    # 长按
    # :param pos x,y
    def long_press(self, pos):
        x, y = pos.split(",", 1)
        TouchAction(self.driver).long_press(None, x, y).perform()

    # 长按
    # :param config {id, class, xpath}
    def long_press_by(self, config):
        ele = self._find_by_any(config)
        TouchAction(self.driver).long_press(ele).perform()

    # 点击按钮
    # :param config {id, class, xpath}
    def click_by(self, config):
        ele = self._find_by_any(config)
        ele.click()

    # 双击按钮
    # :param config {id, class, xpath}
    def double_click_by(self, config):
        ele = self._find_by_any(config)
        ActionChains(self.driver).double_click(ele).perform()

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
        ele = self._find_by_any(config)
        # 文件名
        default_file = str(time.time()).split(".")[0] + ".png" # 默认文件名
        save_file = self._prepare_save_file(config, default_file)
        ele.screenshot(save_file)

    # 执行js
    def execute_js(self, js):
        self.driver.execute_script(js)

    # 返回键
    def back(self, _):
        self.keyevent('4')

    # 模拟系统键
    def keyevent(self, code):
        self.driver.keyevent(code)
        # self.driver.press_keycode(code)

    # 打开手机的通知栏
    def open_notifications(self):
        self.driver.open_notifications()


# cli入口
def main():
    # 基于yaml的执行器
    boot = Boot()
    # 步骤配置的yaml
    if len(sys.argv) > 1:
        step_files = sys.argv[1:]
    else:
        raise Exception("未指定步骤配置文件或目录")
    # 执行yaml配置的步骤
    boot.run(step_files)
    boot.close_driver()


if __name__ == '__main__':
    main()