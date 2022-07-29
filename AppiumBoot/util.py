#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import yaml
import re
import os
import random
from jsonpath import jsonpath
from selenium.webdriver.common.by import By

# 写文本文件
def write_file(path, content, append = False):
    if append:
        mode = 'a'
    else:
        mode = 'w'
    with open(path, mode, encoding="utf-8") as file:
        file.write(content)

# 读文本文件
def read_file(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.read()

# 写二进制文件
def write_byte_file(path, content, append = False):
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    with open(path, mode) as file:
        file.write(content)

# 读二进制文件
def read_byte_file(path):
    with open(path, 'rb') as file:
        return file.read()

# 读yaml配置
# :param yaml_file (步骤配置的)yaml文件
def read_yaml(yaml_file):
    if not os.path.exists(yaml_file):
        raise Exception(f"没找到步骤配置文件: {yaml_file}")
    txt = read_file(yaml_file)
    return yaml.load(txt, Loader=yaml.FullLoader)

# 输出异常
def print_exception(ex):
    print('\033[31m发生异常: ' + str(ex) + '\033[0m')

# 生成一个指定长度的随机字符串
def random_str(n):
    n = int(n)
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(n):
        random_str += base_str[random.randint(0, length)]
    return random_str

# 生成一个指定长度的随机数字
def random_int(n):
    n = int(n)
    random_str = ''
    for i in range(n):
        random_str += str(random.randint(0, 9))
    return random_str

# 自增的值
incr_vals = {}

# 自增值，从1开始
def incr(key):
    if key not in incr_vals:
        incr_vals[key] = 0
    incr_vals[key] = incr_vals[key] + 1
    return incr_vals[key]

# 变量
bvars = {}

# 设置变量
def set_var(name, val):
    bvars[name] = val

# 获取变量
def get_var(name):
    return bvars[name]

# 替换变量： 将 $变量名 或 ${变量表达式} 替换为 变量值
# :param txt 兼容基础类型+字符串+列表+字典等类型, 如果是字符串, 则是带变量的表达式
# :param to_str 是否转为字符串, 否则原样返回, 可能是int/dict之类的, 主要是使用post动作的data是dict变量; 只针对整体匹配的情况
# :return
def replace_var(txt, to_str = True):
    # 如果是基础类型，直接返回
    if isinstance(txt, (int, float, complex, bool)):
        return txt

    # 如果是列表/元组/集合，则每个元素递归替换
    if isinstance(txt, (list, tuple, set)):
        return list(map(replace_var, txt))

    # 如果是字典，则每个元素递归替换
    if isinstance(txt, dict):
        for k, v in txt.items():
            txt[k] = replace_var(v)  # 替换变量
        return txt

    # 字符串：直接替换
    return do_replace_var(txt, to_str)

# 真正的替换变量: 将 $变量名 替换为 变量值
# :param txt 只能接收字符串
# :param txt 是否转为字符串, 否则原样返回, 可能是int/dict之类的, 主要是使用post动作的data是dict变量; 只针对整体匹配的情况
def do_replace_var(txt, to_str = True):
    if not isinstance(txt, str):
        raise Exception("变量表达式非字符串")

    # re正则匹配替换字符串 https://cloud.tencent.com/developer/article/1774589
    def replace(match, to_str = True) -> str:
        r = analyze_var_expr(match.group(1))
        if to_str: # 转字符串
            return str(r)
        return r # 原样返回, 可能是int/dict之类的, 主要是使用post动作的data是dict变量

    # 1 整体匹配: 整个是纯变量表达式
    mat1 = re.match(r'\$([\w\d_]+)', txt)
    mat2 = re.match(r'\$\{([\w\d_\.\(\)]+)\}', txt)
    if mat1 or mat2:
        if mat1:
            mat = mat1
        else:
            mat = mat2
        return replace(mat, to_str)

    # 2 局部匹配: 由 普通字符串 + 变量表达式 组成
    txt = re.sub(r'\$([\w\d_]+)', replace, txt)  # 处理变量 $msg
    txt = re.sub(r'\$\{([\w\d_\.\(\)]+)\}', replace, txt)  # 处理变量 ${data.msg} 或 函数调用 ${random_str(1)}
    return txt

# 解析变量表达式
# :param expr 变量表达式
# :return 表达式的值
def analyze_var_expr(expr):
    # 单独处理
    if '(' in expr:  # 函数调用, 如 random_str(1)
        r = parse_and_call_func(expr)
        return r

    if '.' in expr:  # 有多级属性, 如 data.msg
        return jsonpath(bvars, '$.' + expr)[0]

    return bvars[expr]


# 替换变量时用到的内部函数
funcs = {
    'random_str': random_str,
    'random_int': random_int,
    'incr': incr
}

# 解析并调用函数
def parse_and_call_func(expr):
    mat = re.match(r'([\w\d_]+)\((.+)\)', expr)
    if mat == None:
        raise Exception("不符合函数调用语法: " + expr)

    # 函数名
    func = mat.group(1)
    if func not in funcs:
        raise Exception(f'无效校验函数: {func}')

    # 函数参数
    param = mat.group(2)

    # 调用函数
    return funcs[func](param)

# 类型转by
def type2by(type):
    if type == 'id':
        return By.ID
    if type == 'aid':
        return By.ACCESSIBILITY_ID
    if type == 'class':
        return By.CLASS_NAME
    if type == 'xpath':
        return By.XPATH
    raise Exception(f"不支持查找类型: {type}")