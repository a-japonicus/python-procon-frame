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
from xml.sax.saxutils import *
import ConfigParser
from Cookie import SimpleCookie
from lib.response import Response
from lib.session.session import Session
from lib.tag import *
from page.page import Page
from lib import DBAccess

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

#DBアクセサ生成
DBAccess.create(setting['database'])

#テーブル作成
if setting['database']['create'] == 'On':
    dba = DBAccess.order()
    sqls = [
        'CREATE TABLE session_tbl(session_id CHAR(40) UNIQUE, data BLOB, update_time INTEGER)',
        'CREATE TABLE user_tbl(user_id INTEGER PRIMARY KEY, username CHAR(32) UNIQUE, password CHAR(64), nickname CHAR(32), hash CHAR(64) UNIQUE, login_time INTEGER, create_time INTEGER)',
        'CREATE TABLE problem_tbl(problem_id INTEGER PRIMARY KEY, user_id INTEGER, title CHAR(64), data TEXT, create_time INTEGER)',
    ]
    for s in sqls:
        try:
            dba.execute_sql(s)
        except:
            pass
# セッション
session_handler = None
if setting['session']['handler'] == 'file':
    from lib.session.FileSessionHandler import FileSessionHandler
    session_handler = FileSessionHandler(setting['session'])
elif setting['session']['handler'] == 'database':
    from lib.session.DBSessionHandler import DBSessionHandler
    session_handler = DBSessionHandler(setting['session'])
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
error_info = []
try:
    # ページクラスを動的インポート
    page_class_name = page.capitalize()+'Page'
    page_class = getattr(__import__('page.'+page, {}, {}, page_class_name), page_class_name)
    response_page = page_class(session, setting, form)
    page_data = response_page.make_page()
except:
    import sys
    error_info.append(sys.exc_info())
    response_page = None

# ページクラスが読み込めなければ未実装と判定
if response_page is None:
    response_page = Page(session, setting, form)
    page_data = response_page.make_page()

# HTMLの組立て
response.add_response_data(
    HtmlTag([
        HeadTag(TitleTag(u'高専プロコン競技練習場[%s]' % response_page.get_title())),
        BodyTag([
            CenterTag([
                top,
                HRTag(),
                page_data,
            ])
        ])
    ])
)

session.close()
print (response)

# デバッグ出力
if setting['debug']['enable'] == 'On':
    for info in error_info:
        print (escape(str(info)).encode('utf-8'))
        print('<br>')
    for flist in form.list:
        print (escape(str(flist)).encode('utf-8'))
        print('<br>')
    for k,v in os.environ.items():
        print (k,v)
