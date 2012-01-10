#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        SimpleCGIServer
# Purpose:     CGIHTTPServerを使用した簡易サーバ
#
# Author:      hatahata
#
# Created:     06/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import os
import cgi
from Cookie import SimpleCookie
from lib.request import Request
from lib.MyStrage import MyStrage
from app import AppResponse
from lib import DBAccess
from lib.session import Session

# クッキーのセッションIDキー
COOKIE_SESSIONID = 'SESSIONID'


class App(object):
    """
    WSGI アプリ
    """
    def setting(self):
        """
        設定ファイル読み込み
        """
        import ConfigParser
        CONF_FILE = os.path.join(path.ROOT_DIR, "./setting.conf")
        conf = ConfigParser.SafeConfigParser()
        conf.read(CONF_FILE)
        
        setting = {}
        for section in conf.sections():
            setting[section] = {}
            for option in conf.options(section):
                setting[section][option] = conf.get(section, option)
        return setting
    
    def create_database(self, dba):
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

    def __call__(self, environ, start_response):
        """
        レスポンスのボディを返す。
        
        env
            HTTP リクエストが格納された辞書。
        start_response
            呼び出し可能オブジェクト。
            start_response を使って、ステータスコードとレスポンスヘッダを出力する。
        """
#        import app
#        response = app.response
        # ルーティング情報取得
        route = environ.get('PATH_INFO', '').strip('/').split('/')
        # POSTデータ取出し
        post = {}
        if environ.get('REQUEST_METHOD') == 'POST':
            content_length = environ.get('CONTENT_LENGTH', '')
            if not content_length.isalnum():
                content_length = 0
            else:
                wsgi_input = environ['wsgi.input']
                for value in cgi.parse_qsl(wsgi_input.read(int(content_length))):
                    post[value[0]] = value[1]
        # クッキー
        cookie=SimpleCookie(environ.get('HTTP_COOKIE',''))
#        print(cookie, route, post)
        # 設定
        setting = self.setting()
        # データベース
        DBAccess.create(setting['database'])
        if setting['database']['create'] == 'On':
            self.create_database(DBAccess.order())
        # セッション
        session_id = None
        if COOKIE_SESSIONID in cookie:
            session_id = cookie[COOKIE_SESSIONID].value
        Session.create(setting['session'], session_id)

        session = Session.order()
        dba = DBAccess.order()
  
        # リクエスト情報を設定
        request = Request()
        request.set('Setting', setting)
        request.set('Session', session)
        request.set('DBA', dba)
        request.set('Route', route)
        request.set('Post', MyStrage(post))
        request.set('Cookie', cookie)
        request.set('Environ', environ)
        # レスポンスを作成
        response = AppResponse(request)
        
        # クッキーにセッションIDをセット
        session.close()
        response.set_cookie(COOKIE_SESSIONID, session.get_session_id(), session.get_lifetime())

        # レスポンス
#        print(response.get_header_list())
#        print(response.get_body())
        start_response("200 OK", response.get_header_list())
        return response.get_body()

#        print(response.get_header_list())
#        print(unicode(response.get_body(), response.get_charset()))
#        start_response("200 OK", [("Content-type", "text/plain")])
#        return "Hello world!"


if __name__ == "__main__":
    pass
#    import BaseHTTPServer
#    import CGIHTTPServer
#    from wsgiref import simple_server
#    server = simple_server.make_server("", 80, App())
#    server.serve_forever()
    
    
