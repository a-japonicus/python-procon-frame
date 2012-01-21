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
from xml.sax.saxutils import *
from page import Page
from lib.tag import *
from lib import DBAccess
from lib.user import User

class LoginPage(Page):
    """
    ログインページ出力
    """
    def __init__(self,request):
        self.request = request
        self.session = request['Session']
        self.form_data = request['Post']
        self.setting = request['Setting']
        self.set_title(u'ログイン')
        self.dba = DBAccess.order()
    def index(self, param):
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
            user = User()
            if user.login(username, password, self.setting['password']['salt']):
                # ログイン成功
                self.session.setvalue('login', True)
                self.session.setvalue('user_id', user.getvalue('id'))
                redirect = True


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
        page = CenterTag()
        if data['redirect']:
            return self.redirect('/top')
        elif data['login']:
            page.add_value(PTag(u'ログイン済みです'))
        else:
            page.add_value([
                PTag(u'ログインすると全ての機能を使用できます。未登録の方は%sから登録してください。' % ATag('./regist', u'こちら')),
                FormTag(action='./login', values=[
                    TableTag([
                        TRTag([TDTag(u'ユーザ名'), TDTag(':'), TDTag('%s' % TextTag(name='username', value=escape(data['username'])))]),
                        TRTag([TDTag(u'パスワード'), TDTag(':'), TDTag('%s' % PasswordTag(name='password', value=''))]),
                    ]),
                    HiddenTag(name='mode', value='login'),
                    SubmitTag(value=u'ログイン'),
                ])
            ])
            if data['login_failed']:
                page.add_value(PTag(u'ログインに失敗しました'))

        return self.html_page_template(DivTag('page', [H2Tag(u'ログイン画面'),page]))


if __name__ == '__main__':
    pass
