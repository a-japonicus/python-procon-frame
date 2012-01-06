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
import path
import cgi
import os
import atexit
import ConfigParser
from Cookie import SimpleCookie
from response import Response
from session import Session
from tag import *
from page import Page
from db_session_handler import DBSessionHandler

form = cgi.FieldStorage()
cookie=SimpleCookie(os.environ.get('HTTP_COOKIE',''))


CONF_FILE = os.path.join(os.path.dirname(__file__), "../setting.conf")
conf = ConfigParser.SafeConfigParser()
conf.read(CONF_FILE)

# セッション設定
session_setting = {}
for k,v in conf.items('session'):
    session_setting[k] = v;
session_handler_setting = {}
for k,v in conf.items('session_handler'):
    session_handler_setting[k] = v;

session_handler = DBSessionHandler(session_handler_setting)
session = Session(cookie, session_handler, session_setting)


response = Response(cookie)
page = form.getvalue('page', 'top')

#トップ部分作成
top = DivTag('top')
top.add_value(H1Tag(u'高専プロコン競技練習場'))
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

# HTMLの組立て
response.add_response_data(
    HtmlTag(values=[
        HeadTag(TitleTag(u'高専プロコン競技練習場[%s]' % response_page.get_title())),
        BodyTag(values=[
            top,
            HRTag(),
            response_page.make_page(),
        ])
    ])
)
session.close()
print (response)
