#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 常量定义
Desc : 
"""
from scrapy_site.utils import const

# 编码
const.ENCODE = 'UTF-8'
# 检索关键字配置文件
const.KEYWORD_CONF = 'keyword.conf'
# 网站名称关键字
const.WEBNAME_CONF = 'webname.conf'
# email收件人配置文件
const.EMAIL_CONF = 'email.conf'

# 第三方 SMTP 服务
const.MAIL_HOST = "smtp.163.com"  # 设置服务器
# 发送者Email地址
const.SENDER = 'xxxx@163.com'
# 发送者Email用户名
const.MAIL_USER = "xxxx"  # 用户名
# 发送者Email密码
const.MAIL_PASS = "xxxx"  # 口令 需要授权码
