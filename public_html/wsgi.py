#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        WSGI
# Purpose:     WSGIを使ったWebアプリ
#
# Author:      hatahata
#
# Created:     06/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import cgi
from Cookie import SimpleCookie
from xml.sax.saxutils import *
from lib.MyStrage import MyStrage
from lib import DBAccess
from lib.session import Session
from lib.tag import *

class App(object):
    """
    WSGI アプリ
    """
    def setting(self):
        """
        設定ファイル読み込み
        """
        import ConfigParser
        CONF_FILE = os.path.join(os.getcwd(), "../setting.conf")
        conf = ConfigParser.SafeConfigParser()
        conf.read(CONF_FILE)

        setting = {}
        for section in conf.sections():
            setting[section] = {}
            for option in conf.options(section):
                setting[section][option] = conf.get(section, option)
        return setting

    def create_table(self, dba):
        """
        テーブル作成
        """
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
    def routing(self, request):
        """
        ルーティング
        """
        route = request.getvalue('Route', ['top'])
        session = request.getvalue('Session', None)
        setting = request.getvalue('Setting', {})
        post = request.getvalue('Post', MyStrage())

        # ルーティング情報がなければデフォルトをセット
        if route[0] == '':
            route = ['top']
        if len(route)<2:
            route.append('index')
        elif route[1]=='':
            route[1] = 'index'

        page = route[0]
        method = route[1]
        param = []
        for i in range(len(route)-2):
            param.append(route[i+2])

        # ページクラスを取得
        response_page = None
        try:
            # ページクラスを動的インポート
            page_class_name = page.capitalize()+'Page'
            page_class = getattr(__import__('page.'+page, {}, {}, page_class_name), page_class_name)
            response_page = page_class(request)
        except:
            import sys
            self.error_info.append(sys.exc_info())
            response_page = None

        # ページクラスが読み込めなければ未実装と判定
        if response_page is None:
            from page.page import Page
            response_page = Page(request)

        # ページからメソッド取得
        try:
            response_method = getattr(response_page, method)
            page_data = response_method(param)
        except:
            import sys
            self.error_info.append(sys.exc_info())
            response_method = getattr(response_page, 'error')
            page_data = response_method(param)

        self.title = response_page.get_title()

        return page_data


    def debug(self):
        """
        デバッグ
        """
        # デバッグ出力
        debug_output = DivTag('debug',Tag('font', H3Tag(u'デバッグモード'), {'color':'red'}))
        # SESSION
        session_items = self.request.getvalue('Session',{}).items()
        if len(session_items) > 0:
            session_list = PTag(Tag('font', Tag('b','SESSION: '), {'size':3}))
            for name,value in session_items:
                session_list.add_value(escape(unicode('%s => %s, ' % (name, value), 'utf-8')))
            debug_output.add_value(session_list)
        # POST
        post_list = PTag(Tag('font', Tag('b','POST: '), {'size':3}))
        post = self.request.getvalue('Post', {})
        post_items = post.items()
        if len(post_items) > 0:
            for name,value in post_items:
                post_list.add_value(escape(unicode('%s => %s, ' % (name, value), 'utf-8')))
            debug_output.add_value(post_list)
        # ERROR
        if len(self.error_info) > 0:
            error_list = PTag(Tag('font', Tag('b','ERROR: '), {'size':3}))
            for info in self.error_info:
                error_list.add_value(escape('%s, ' % str(info)))
            debug_output.add_value(error_list)

        return CenterTag(debug_output)

    def __call__(self, environ, start_response):
        """
        レスポンスのボディを返す。
        environ
            HTTP リクエストが格納された辞書。
        start_response
            呼び出し可能オブジェクト。
            start_response を使って、ステータスコードとレスポンスヘッダを出力する。
        """
        self.error_info = []
        # 設定
        setting = self.setting()
        # ルーティング情報取得
        route = environ.get('PATH_INFO', '').strip('/').split('/')
        # POSTデータ取出し
        post = MyStrage()
        if environ.get('REQUEST_METHOD') == 'POST':
            content_length = environ.get('CONTENT_LENGTH', '')
            if not content_length.isalnum():
                content_length = 0
            else:
                wsgi_input = environ['wsgi.input']
                input_parse = cgi.parse_qsl(wsgi_input.read(int(content_length)))
                for value in input_parse:
                    post.setvalue(value[0], value[1])
        # データベース
        dba = DBAccess.create(setting['database'])
        if setting['database']['create'] == 'On':
            self.create_table(dba)
        # クッキー
        cookie=SimpleCookie(environ.get('HTTP_COOKIE',''))
        # セッション
        session_id = None
        if setting['session']['id'] in cookie:
            session_id = cookie[setting['session']['id']].value
        session = Session.create(setting['session'], session_id)

        # リクエスト情報を設定
        request = MyStrage()
        request.setvalue('Setting', setting)
        request.setvalue('Session', session)
        request.setvalue('DBA', dba)
        request.setvalue('Route', route)
        request.setvalue('Post', post)
        request.setvalue('Cookie', cookie)
        request.setvalue('Environ', environ)

        self.request = request

        # レスポンスを作成
        response = self.routing(request)

        #デバッグ出力
        debug_output = ''
        if setting['debug']['enable'] == 'On':
            debug_output = self.debug()

        session.close()

        response_header =[('Content-type', 'text/html;charset=utf-8')]
        if session.get_session_id():
            # クッキーにセッションIDをセット
            response_header.append(('Set-Cookie', '%s=%s'%(setting['session']['id'],session.get_session_id())))


        # レスポンス
        print(response_header)
        print(u'%s'%debug_output)
        print(u'%s'%response)
        start_response("200 OK", response_header)
        return (u'%s%s'%(debug_output,response)).encode('utf-8')


if __name__ == "__main__":
    pass

