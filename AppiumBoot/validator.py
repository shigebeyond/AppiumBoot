#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from AppiumBoot.response_wrapper import ResponseWrap
from selenium import webdriver
from requests import Response
from pyutilb import log

# 校验器
class Validator(ResponseWrap):

    def __init__(self, driver: webdriver.Remote, res: Response = None):
        super(Validator, self).__init__(driver, res)
        # 校验函数映射
        self.funcs = {
            '=': lambda val, param: val == param,
            '>': lambda val, param: float(val) > param,
            '<': lambda val, param: float(val) < param,
            '>=': lambda val, param: float(val) >= param,
            '<=': lambda val, param: float(val) <= param,
            'contains': lambda val, param: param in val,
            'startswith': lambda val, param: val.startswith(param),
            'endswith': lambda val, param: val.endswith(param),
            'regex_match': lambda val, param: re.search(param, val) != None,
        }

    # 执行校验
    def run(self, config):
        if self.res != None:
            if 'validate_by_jsonpath' in config:
                return self.run_type('jsonpath', config['validate_by_jsonpath'])

            if 'validate_by_css' in config:
                return self.run_type('css', config['validate_by_css'])

        if 'validate_by_xpath' in config:
            return self.run_type('xpath', config['validate_by_xpath'])

        if 'validate_by_id' in config:
            return self.run_type('id', config['validate_by_id'])

        if 'validate_by_aid' in config:
            return self.run_type('aid', config['validate_by_aid'])

        if 'validate_by_class' in config:
            return self.run_type('class', config['validate_by_class'])

    # 执行单个类型的校验
    def run_type(self, type, fields):
        for path, rules in fields.items():
            # 校验单个字段
            self.run_field(type, path, rules)

    # 执行单个字段的校验
    def run_field(self, type, path, rules):
        # 获得字段值
        val = self._get_val_by(type, path)
        # 逐个函数校验
        for func, param in rules.items():
            b = self.run_func(func, val, param)
            if b == False:
                raise Exception(f"响应元素[{path}]不满足校验条件: {val} {func} '{param}'")

    '''
    执行单个函数：就是调用函数
    :param func 函数名
    :param val 校验的值
    :param param 参数
    '''
    def run_func(self, func, val, param):
        if func not in self.funcs:
            raise Exception(f'无效校验函数: {func}')
        # 调用校验函数
        log.debug(f"处理校验函数: {func}={param}")
        func = self.funcs[func]
        return func(val, param)