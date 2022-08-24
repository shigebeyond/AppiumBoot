#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from pyutilb.util import *
from lxml import etree
from requests import Response
from selenium import webdriver
from jsonpath import jsonpath
from selenium.webdriver.common.by import By

# 响应包装器
class ResponseWrap(object):

    def __init__(self, driver: webdriver.Remote, res: Response = None):
        # webdriver
        self.driver = driver
        # 响应
        self.res = res

    # 获得元素值
    def _get_val_by(self, type, path):
        if type == 'css':
            path, prop = split_xpath_and_prop(path)
            if self.res != None:
                html = etree.fromstring(self.res.text, etree.HTMLParser())
                ele = html.cssselect(path)[0]
                return self.get_prop_or_text(ele, prop)

            raise Exception(f"无http响应, 不支持查找类型: {type}")

        if type == 'xpath':
            path, prop = split_xpath_and_prop(path)
            if self.res != None:
                html = etree.fromstring(self.res.text, etree.HTMLParser())
                ele = html.xpath(path)[0]
            else:
                ele = self.driver.find_element(By.XPATH, path)
            return self.get_prop_or_text(ele, prop)

        if type == 'jsonpath':
            if self.res != None:
                data = self.res.json()
                return jsonpath(data, path)[0]

            raise Exception(f"无http响应, 不支持查找类型: {type}")

        if type == 'id' or type == 'aid' or type == 'class':
            return self.driver.find_element(type2by(type), path).get_text_or_content()

        raise Exception(f"不支持查找类型: {type}")

    # 获得元素的属性值或文本
    def get_prop_or_text(self, ele, prop):
        # 1 响应元素
        if isinstance(ele, etree._Element):
            if prop != '':  # 获得属性
                return ele.get(prop)
            return ele.text

        # 2 页面元素
        if prop != '':  # 获得属性
            return ele.get_attribute(prop)
        return ele.get_text_or_content()
