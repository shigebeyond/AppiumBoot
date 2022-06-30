# -*- coding: utf-8 -*-
'''
网易的orc
调用
https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
'''

import sys
import uuid
import requests
import base64
import hashlib

from imp import reload

import time

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/ocrapi'
APP_KEY = '29521b6013cd28f7'
APP_SECRET = 'znz3CV3W7grWbEkrjPxcYZfEwOeLyqNb'


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

# 识别图片中的文字
def recognize_text(file):
    f = open(file, 'rb')  # 二进制方式打开图文件
    q = base64.b64encode(f.read()).decode('utf-8')  # 读取文件内容，转换为base64编码
    f.close()

    data = {}
    data['detectType'] = '10012'
    data['imageType'] = '1'
    data['langType'] = 'en'
    data['img'] = q
    data['docType'] = 'json'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    result = response.json()
    if int(result['errorCode']) > 0:
        raise Exception(f"调用有道orc接口错误: {result}")

    return result['Result']['regions'][0]['lines'][0]['text']

'''
正常响应
{
    "requestId":"afd3a745-9753-4767-b672-da1c81d750fa",
    "errorCode":"0",
    "Result":{
        "orientation":"UP",
        "regions":[
            {
                "boundingBox":"15,0,98,0,98,48,15,48",
                "dir":"h",
                "lang":"en",
                "lines":[
                    {
                        "boundingBox":"15,0,98,0,98,48,15,48",
                        "text_height":48,
                        "words":[
                            {
                                "boundingBox":"15,0,98,0,98,48,15,48",
                                "word":"2697"
                            }
                        ],
                        "text":"2697",
                        "lang":"en"
                    }
                ]
            }
        ],
        "exif":"UP",
        "scene":"other"
    }
}
'''

if __name__ == '__main__':
    recognize_text('./test.jpg')