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
from page import Page
from session import Session
from tag import *

class LoginPage(Page):
    """
    ログインページ出力
    """
    def __init__(self, session, form_data=None):
        super(LoginPage, self).__init__(u'ログイン', form_data)
        self.set_session(session)
    def make_page(self):
        username = self.form_data.getvalue('username', '')
        password = self.form_data.getvalue('password', '')
        mode = self.form_data.getvalue('mode')
        login = False;
        redirect = False

        if self.session.getvalue('login', False):
            login = True
        else:
            if mode == 'login':
                if username.isalnum() and password.isalnum():
                    if username == 'user' and password == 'pass':
                        # ここで認証＆リダイレクト
                        self.session.regenerate_id()
                        self.session.setvalue('login', True)
                        login = True
                        redirect = True

        # テンプレ―ト用データ
        template_data = {}
        template_data['mode'] = mode
        template_data['redirect'] = redirect
        template_data['login'] = login
        template_data['username'] = username

        return self.template(template_data)

    def template(self, data):
        page = DivTag('page')
        if data['redirect']:
#            page.add_value(RedirectTag('./index.py?page=top'))
            pass
        elif data['login']:
            page.add_value(PTag(u'ログイン済みです'))
        else:
            page.add_value(H2Tag(u'ログイン画面'))
            regist_link = ATag('./index.py?page=regist', u'こちら')
            page.add_value(PTag(u'ログインするとランキングに表示されます。未登録の方は%sから登録してください。' % regist_link))
            form_tag = FormTag(action='./index.py?page=login')
            form_tag.add_value(u'ユーザ名:%s<br>' % TextTag(name='username', value=data['username']))
            form_tag.add_value(u'パスワード:%s<br>' % PasswordTag(name='password', value=''))
            form_tag.add_value(HiddenTag(name='mode', value='login'))
            form_tag.add_value(SubmitTag(value=u'ログイン'))
            page.add_value(form_tag)
            if data['mode'] == 'login':
                page.add_value(u'ログインに失敗しました')

        return page


if __name__ == '__main__':
#    login_page = LoginPage()
#    print('%s'.encode('utf-8') % login_page)
    pass
