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
from lib.response import Response
from lib.session.session import Session
from lib.tag import *
from page.page import Page

form = cgi.FieldStorage()
cookie=SimpleCookie(os.environ.get('HTTP_COOKIE',''))

#cookie['SESSIONID'] = 'b9c34db31dcd13db6de0f7dad1474397'

# 設定ファイル読み込み
CONF_FILE = os.path.join(os.path.dirname(__file__), "../setting.conf")
conf = ConfigParser.SafeConfigParser()
conf.read(CONF_FILE)

setting = {}
for section in conf.sections():
    setting[section] = {}
    for option in conf.options(section):
        setting[section][option] = conf.get(section, option)

# セッション
session_handler = None
if setting['session']['handler'] == 'file':
    from lib.session.file_session_handler import FileSessionHandler
    session_handler = FileSessionHandler(setting['session'])
elif setting['session']['handler'] == 'database':
    from lib.session.db_session_handler import DBSessionHandler
    session_handler = DBSessionHandler(setting['database'])
session = Session(cookie, session_handler, setting['session'])

# レスポンス作成開始
response = Response(cookie)
page = form.getvalue('page', 'top')

#トップ部分作成
top = DivTag('top')
top.add_value(H1Tag(u'高専プロコン競技練習場'))
if session.getvalue('login', False):
    top.add_value(PTag(u'ログイン中です'))
top_links = [('top', u'トップ'), ('edit', u'問題作成'), ('bbs', u'掲示板'), ('about', u'取扱説明書'), ('profile', u'プロフィール'), ('regist', u'登録'), ('logout', u'ログアウト'), ('login', u'ログイン'), ('admin', u'管理画面')]
for p in top_links:
#    if page != p[0]:
        top.add_value(u'[%s]' % ATag('./index.py?page=%s'%p[0], p[1]))
#    else:
#        top.add_value(u'[%s]' % p[1])

# ページクラスを取得
response_page = None
error_info = ""
try:
    # ページクラスを動的インポート
    page_class_name = page.capitalize()+'Page'
    page_class = getattr(__import__('page.'+page, {}, {}, page_class_name), page_class_name)
    response_page = page_class(session, setting, form)
except:
    import sys
    error_info = sys.exc_info()
    response_page = None

# ページクラスが読み込めなければ未実装と判定
if response_page is None:
    response_page = Page(session, setting, form)

# HTMLの組立て
response.add_response_data(
    HtmlTag([
        HeadTag(TitleTag(u'高専プロコン競技練習場[%s]' % response_page.get_title())),
        BodyTag([
            CenterTag([
                top,
                HRTag(),
                response_page.make_page(),
            ])
        ])
    ])
)

session.close()
print (response)

# デバッグ出力
if setting['debug']['enable'] == 'On':
    print (error_info)
