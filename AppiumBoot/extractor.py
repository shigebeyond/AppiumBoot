#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests import Response
from selenium import webdriver
from AppiumBoot.response_wrapper import ResponseWrap
from pyutilb.util import *
import json # eval 可能会用到
import re
from pyutilb import log

# 抽取器
class Extractor(ResponseWrap):

    def __init__(self, driver: webdriver.Remote, res: Response = None):
        super(Extractor, self).__init__(driver, res)

    # 抽取参数
    def run(self, config):
        if self.res != None:
            if 'extract_by_jsonpath' in config:
                return self.run_type('jsonpath', config['extract_by_jsonpath'])

            if 'extract_by_css' in config:
                return self.run_type('css', config['extract_by_css'])

        if 'extract_by_xpath' in config:
            return self.run_type('xpath', config['extract_by_xpath'])

        if 'extract_by_id' in config:
            return self.run_type('id', config['extract_by_id'])

        if 'extract_by_aid' in config:
            return self.run_type('aid', config['extract_by_aid'])

        if 'extract_by_class' in config:
            return self.run_type('class', config['extract_by_class'])

        if 'extract_by_eval' in config:
            return self.run_eval(config['extract_by_eval'])

    # 执行单个类型的抽取
    def run_type(self, type, fields):
        for var, path in fields.items():
            # 获得字段值
            val = self._get_val_by(type, path)
            # 抽取单个字段
            set_var(var, val)
            log.debug(f"从响应中抽取参数: {var}={val}")

    # 执行eval类型的抽取
    def run_eval(self, fields):
        for var, expr in fields.items():
            # 获得字段值
            val = eval(expr, globals(), bvars) # 丢失本地与全局变量, 如引用不了json模块
            # 抽取单个字段
            set_var(var, val)
            log.debug(f"抽取参数: {var}={val}")

