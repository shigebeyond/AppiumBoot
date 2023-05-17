#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests import Response
from selenium import webdriver
from AppiumBoot.response_wrapper import ResponseWrap
from pyutilb.util import *
from pyutilb.file import *
import json # eval 可能会用到
import re
from pyutilb.log import log
from pyutilb import BaseExtractor

# 抽取器
class Extractor(BaseExtractor, ResponseWrap):

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
            return self.run_type('eval', config['extract_by_eval'])
