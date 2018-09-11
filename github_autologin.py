#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: github_autologin.py
@time: 2018/9/11 11:43
@desc: Github自动登陆
'''

import requests
import bs4
import sys

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'}

login_response = requests.get('https://github.com/login')
cookies_one = login_response.cookies.get_dict()
soup = bs4.BeautifulSoup(login_response.text, features= 'html.parser')
token_tag = soup.find(name='input', attrs= {'name' : 'authenticity_token'}) # type: bs4.element.Tag
# 认证token
authenticity_token = token_tag.get('value')

from_data = {
    'utf8': '',
    'authenticity_token' : authenticity_token,
    'login' : input('请输入账号:'),
    'password' : input('请输入密码:'),
    'commit': 'Sign in'
}

# 正式登陆
seesion_login_response =  requests.post(
    url = 'https://github.com/session',
    data = from_data,
    cookies = cookies_one
)
cookies_two = seesion_login_response.cookies.get_dict()
cookies_one.update(cookies_two)

login_soup = bs4.BeautifulSoup(seesion_login_response.text, features= 'html.parser')
current_user_tag = login_soup.find(name='strong', attrs= {'class': 'css-truncate-target'})
if not current_user_tag:
    print('登陆失败,请检查用户名和密码')
    sys.exit()
# 获取自己的github名称
current_user = current_user_tag.text

repositories_response = requests.get(
    url= "https://github.com/" + current_user + "?tab=repositories",
    cookies = cookies_one
)
repositories_soup = bs4.BeautifulSoup(repositories_response.text, features= 'html.parser')
# 遍历输出所有仓库名称
repositories_list = repositories_soup.find_all(name= 'a', attrs= {'itemprop': 'name codeRepository'})
for element in repositories_list:
    print(element.text.lstrip().rstrip())
