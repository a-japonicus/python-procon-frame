#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        login.py
# Purpose:     ログインページ
#
# Author:      hatahata
#
# Created:     31/12/2011
# Copyright:   (c) hatahata 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import hashlib
from page import Page
from session import Session
from tag import *
from db_access import DBAccess

SALT = 'da894qwnchriuoqc489qoyt9ae'

class LoginPage(Page):
    """
    ログインページ出力
    """
    def __init__(self, session, setting, form_data=None):
        super(LoginPage, self).__init__(session, setting, form_data)
        self.set_title(u'ログイン')
        self.set_session(session)
        self.dba = DBAccess(setting['database'])
    def login(self, username, password):
        """
        ログイン認証
        """
        if username is None or password is None:
            return False
        if not username.isalnum() or not password.isalnum():
            return False
        pass_hash = hashlib.sha256(SALT + username + ':' + password).hexdigest()
        if len(self.dba.select(table='user_tbl', where={'username':username, 'password':pass_hash})) != 1:
            return False
        return True
    def make_page(self):
        """
        ページの処理
        """
        username = self.form_data.getvalue('username', '')
        password = self.form_data.getvalue('password', None)
        mode = self.form_data.getvalue('mode')
        login = False;
        redirect = False
        login_failed = False

        if not username.isalnum():
            username = ''

        if self.session.getvalue('login', False):
            login = True
        elif mode == 'login':
            login_failed = True
            if self.login(username, password):
                # ログイン成功
                self.session.setvalue('login', True)
                redirect = True
                login_failed = False

        # テンプレ―ト用データ
        template_data = {}
        template_data['mode'] = mode
        template_data['redirect'] = redirect
        template_data['login'] = login
        template_data['login_failed'] = login_failed
        template_data['username'] = username

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'ログイン画面'))
        if data['redirect']:
            page.add_value(RedirectTag('./index.py?page=top'))
        elif data['login']:
            page.add_value(PTag(u'ログイン済みです'))
        else:
            page.add_value([
                PTag(u'ログインすると全ての機能を使用できます。未登録の方は%sから登録してください。' % ATag('./index.py?page=regist', u'こちら')),
                FormTag(action='./index.py?page=login', values=[
                    u'ユーザ名:%s<br>' % TextTag(name='username', value=data['username']),
                    u'パスワード:%s<br>' % PasswordTag(name='password', value=''),
                    HiddenTag(name='mode', value='login'),
                    SubmitTag(value=u'ログイン'),
                ])
            ])
            if data['login_failed']:
                page.add_value(PTag(u'ログインに失敗しました'))

        return page


if __name__ == '__main__':
    pass
