#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        regist
# Purpose:     ユーザ登録画面
#
# Author:      hatahata
#
# Created:     07/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
from xml.sax.saxutils import *
from page import Page
from lib.tag import *
from lib import DBAccess
from lib.user import User

class RegistPage(Page):
    """
    ユーザ登録ページ出力
    """
    def __init__(self,request):
        self.request = request
        self.session = request['Session']
        self.setting = request['Setting']
        self.form_data = request['Post']
        self.set_title(u'登録')
        self.dba = DBAccess.order()
    def regist(self, username, password):
        """
        登録
        """
        user = User(username)
        if user.exist():
            return False
        user.setvalue('username', username)
        user.setvalue('nickname', u'名無し')
        user.reset_hash()
        if not user.reset_password(new_password=password, salt=self.setting['password']['salt'], force=True):
            return False
        return user.insert()

    def index(self, param):
        """
        ページの処理
        """
        username = self.form_data.getvalue('username', '')
        password = self.form_data.getvalue('password', None)
        retype_password = self.form_data.getvalue('retype_password', None)
        mode = self.form_data.getvalue('mode')
        login = False;
        regist = False
        regist_failed = False

        if not username.isalnum():
            username = ''

        if self.session.getvalue('login', False):
            login = True
        elif mode == 'regist':
            regist_failed = True
            user_id = self.regist(username, password)
            if password == retype_password  and  user_id:
                # ここで登録
                self.session.setvalue('login', True)
                self.session.setvalue('user_id', user_id)
                regist = True
                regist_failed = False


        # テンプレ―ト用データ
        template_data = {}
        template_data['mode'] = mode
        template_data['login'] = login
        template_data['regist'] = regist
        template_data['regist_failed'] = regist_failed
        template_data['username'] = username

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'登録画面'))
        if data['login']:
            page.add_value(PTag(u'ログインしています'))
        elif data['regist']:
            page.add_value(PTag(u'登録しました。%sからプロフィールの変更を行うことができます。ニックネームを設定することをお勧めします。' % ATag('./profile', u'こちら')))
        else:
            page.add_value([
                PTag(u'登録すると全ての機能を使用できます。登録済みの方は%sからログインしてください。' % ATag('./login', u'こちら')),
                FormTag(action='./regist', values=[
                    TableTag([
                        TRTag([TDTag(u'ユーザ名'), TDTag(':'), TDTag('%s' % TextTag(name='username', value=escape(data['username'])))]),
                        TRTag([TDTag(u'パスワード'), TDTag(':'), TDTag('%s' % PasswordTag(name='password', value=''))]),
                        TRTag([TDTag(u'パスワード(再確認)'), TDTag(':'), TDTag('%s' % PasswordTag(name='retype_password', value=''))]),
                    ]),
                    HiddenTag(name='mode', value='regist'),
                    SubmitTag(value=u'登録'),
                ])
            ])
            if data['regist_failed']:
                page.add_value(PTag(u'登録に失敗しました'))

        return self.html_page_template(page)


if __name__ == '__main__':
    pass
