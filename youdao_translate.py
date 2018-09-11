#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: youdao_translate.py
@time: 2018/9/11 14:14
@desc: 利用有道翻译实现简单翻译程序
'''

import requests
import time
import hashlib

# md5加密
def md5(key):
    if not isinstance(key, str):
        print('传入的参数不是字符串')
    else:
        m = hashlib.md5()
        """:type: _hashlib.HASH"""
        m.update(key.encode('utf-8'))
        return m.hexdigest()

# sign: n.md5("fanyideskweb" + e + t + "6x(ZHw]mwzX#u0V7@yfwK")
def translate(keyword):
    u = 'fanyideskweb' #网页或者客户端
    thetimestamp = str(int(time.time()) * 1000) # 当前时间戳（ms）
    c = '6x(ZHw]mwzX#u0V7@yfwK'
    sign = md5(u + keyword + thetimestamp + c) # 签名
    data = {
        'i' : keyword,
        'form' : 'AUTO',
        'to' : 'AUTO',
        'smartresult' : 'dict',
        'client' : u,
        'salt' : thetimestamp,
        'sign' : sign,
        'doctype' : 'json',
        'version' : '2.1',
        'keyfrom' : 'fanyi.web',
        'action' : 'FY_BY_CLICKBUTTION', # 点击按钮提交方式
        'typoResult' : 'true'
    }

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'Origin' : 'http://fanyi.youdao.com',
        'Referer' : 'http://fanyi.youdao.com/'
    }

    response = requests.post(
        url= 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule', # 去掉_o
        headers = headers,
        data = data
    ).json()
    # print(response)
    result = response['translateResult'][0][0]['tgt']
    print('翻译的结果是：%s'%(result))


if __name__ == '__main__':
    while True:
        keyword = input("请输入你要翻译的文字('quit':退出): ").strip()
        if keyword == 'quit':
            break
        translate(keyword)