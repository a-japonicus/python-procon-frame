#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        index
# Purpose:
#
# Author:      hatahata
#
# Created:     31/12/2011
# Copyright:   (c) hatahata 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cgi
import os
from Cookie import SimpleCookie
from response import Response
from session import Session
from tag import *
from page import Page
from db_session_handler import DBSessionHandler

form = cgi.FieldStorage()
cookie=SimpleCookie(os.environ.get('HTTP_COOKIE',''))


response = Response(cookie)

handler_setting={
    'sql_setting':{
        'sql':'sqlite',
        'db':'session.db',
    },
    'session_limit':1440
}
session_setting = {}
session_handler = DBSessionHandler(handler_setting)
session = Session(cookie, session_handler, session_setting)
page = form.getvalue('page', 'top')

top = DivTag('top')
#トップ部分作成
top.add_value(H1Tag(u'高専プロコン2012競技練習場'))
for p in [('top', u'トップ'), ('edit', u'問題作成'), ('about', u'取扱説明書'), ('bbs', u'掲示板'), ('profile', u'プロフィール'), ('regist', u'登録'), ('login', u'ログイン')]:
#    if page != p[0]:
        top.add_value(u'[%s]' % ATag('./index.py?page=%s'%p[0], p[1]))
#    else:
#        top.add_value(u'[%s]' % p[1])

# ページクラスを取得
response_page = None
try:
    if page == 'top':
        pass
    elif page == 'edit':
        pass
    elif page == 'about':
        pass
    elif page == 'bbs':
        pass
    elif page == 'profile':
        pass
    elif page == 'regist':
        pass
    elif page == 'login':
        from login import LoginPage
        response_page = LoginPage(session, form)
except:
    response_page = None

# ページがなければ未実装と判定
if response_page == None:
    response_page = Page()

title = TitleTag(u'高専プロコン2012競技練習場[%s]' % response_page.get_title())

head = HeadTag()
head.add_value(title)

body = BodyTag()
body.add_value(top)
body.add_value(HRTag())
body.add_value(response_page.make_page_data())

html = HtmlTag()
html.add_value(head)
html.add_value(body)

response.add_response_data(html)
session.save()
print (response)
