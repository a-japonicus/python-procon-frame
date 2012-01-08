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
import hashlib
import uuid
from page import Page
from lib.session.session import Session
from lib.tag import *
from lib.db_access import DBAccess

class RegistPage(Page):
    """
    ユーザ登録ページ出力
    """
    def __init__(self, session, setting, form_data=None):
        super(RegistPage, self).__init__(session, setting, form_data)
        self.set_title(u'登録')
        self.set_session(session)
        self.dba = DBAccess(setting['database'])
        self.create_table()
    def create_table(self):
        try:
            self.dba.execute_sql('CREATE TABLE user_tbl(user_id INTEGER PRIMARY KEY, username CHAR(32) UNIQUE, password CHAR(64), nickname CHAR(32), hash CHAR(64) UNIQUE, login_time INTEGER, regist_time INTEGER)')
        except:
            pass
    def regist(self, username, password):
        """
        登録
        """
        if username is None or password is None:
            return False
        if not username.isalnum() or not password.isalnum():
            return False
        if len(self.dba.select(table='user_tbl', where={'username':username})) > 0:
            return False
        pass_hash = hashlib.sha256(self.setting['password']['salt'] + username + ':' + password).hexdigest()
        userhash = hashlib.md5(str(uuid.uuid4())).hexdigest()
        if self.dba.insert('user_tbl', {'username':username, 'password':pass_hash, 'nickname':u'名無しさん', 'hash':userhash}) != 1:
            self.dba.rollback()
            return False
        self.dba.commit()
        return True
    def make_page(self):
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
            if password == retype_password  and  self.regist(username, password):
                # ここで登録
                self.session.setvalue('login', True)
                self.session.setvalue('username', username)
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
            page.add_value(PTag(u'登録しました。%sからプロフィールの変更を行うことができます。ニックネームを設定することをお勧めします。' % ATag('./index.py?page=profile', u'こちら')))
        else:
            page.add_value([
                PTag(u'登録すると全ての機能を使用できます。登録済みの方は%sからログインしてください。' % ATag('./index.py?page=login', u'こちら')),
                FormTag(action='./index.py?page=regist', values=[
                    TableTag([
                        TRTag([TDTag(u'ユーザ名'), TDTag(':'), TDTag('%s' % TextTag(name='username', value=data['username']))]),
                        TRTag([TDTag(u'パスワード'), TDTag(':'), TDTag('%s' % PasswordTag(name='password', value=''))]),
                        TRTag([TDTag(u'パスワード(再確認)'), TDTag(':'), TDTag('%s' % PasswordTag(name='retype_password', value=''))]),
                    ]),
                    HiddenTag(name='mode', value='regist'),
                    SubmitTag(value=u'登録'),
                ])
            ])
            if data['regist_failed']:
                page.add_value(PTag(u'登録に失敗しました'))

        return page


if __name__ == '__main__':
    pass
