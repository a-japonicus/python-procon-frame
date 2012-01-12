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
import path
import os
import cgi
from Cookie import SimpleCookie
from lib.request import Request
from lib.MyStrage import MyStrage
from lib.AppResponse import AppResponse
from lib import DBAccess
from lib.session import Session

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

    def __call__(self, environ, start_response):
        """
        レスポンスのボディを返す。
        environ
            HTTP リクエストが格納された辞書。
        start_response
            呼び出し可能オブジェクト。
            start_response を使って、ステータスコードとレスポンスヘッダを出力する。
        """
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
        # クッキー
        cookie=SimpleCookie(environ.get('HTTP_COOKIE',''))
        # 設定
        setting = self.setting()
        # データベース
        dba = DBAccess.create(setting['database'])
        if setting['database']['create'] == 'On':
            self.create_table(dba)
        # セッション
        session_id = None
        if setting['session']['id'] in cookie:
            session_id = cookie[setting['session']['id']].value
        session = Session.create(setting['session'], session_id)

        # リクエスト情報を設定
        request = Request()
        request.set('Setting', setting)
        request.set('Session', session)
        request.set('DBA', dba)
        request.set('Route', route)
        request.set('Post', post)
        request.set('Cookie', cookie)
        request.set('Environ', environ)
        # レスポンスを作成
        response = AppResponse(request)

        # クッキーにセッションIDをセット
        session.close()
        response.set_cookie(setting['session']['id'], session.get_session_id(), session.get_lifetime())

        # レスポンス
        start_response("200 OK", response.get_header_list())
        return response.get_body()


if __name__ == "__main__":
    pass

