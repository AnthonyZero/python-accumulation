#!/usr/bin/env python
# encoding: utf-8
'''
@author: AnthonyZero
@file: twilio_sms.py
@time: 2018/10/25 15:36
@desc: 利用Twilio免费发送短信
'''

from twilio.rest import Client

# 下面信息在twilio帐号内
account = "xxxxxxxxxxxxxxxxxxxxxxxx"
token = "xxxxxxxxxxxxxxxxxxxxxxxxxx"

# 发送短信 免费帐号不能发短信给没有验证的号码
def send_sms(to_phone, from_phone, body):
    client = Client(account, token)
    message = client.messages.create(
        to= to_phone, # 接收人的手机 手机号需要验证才能发送 https://www.twilio.com/console/phone-numbers/verified
        from_= from_phone, # twilio分配给自己的手机号 固定
        body= body)
    return message;

if __name__ == '__main__':
    message = send_sms('+86158xxxxxxxx','+18135364131','玩转Python之发短信')
    print(message)