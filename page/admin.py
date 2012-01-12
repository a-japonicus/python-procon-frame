#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        admin
# Purpose:     管理画面
#
# Author:      hatahata
#
# Created:     08/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import hashlib
from xml.sax.saxutils import *
from page import Page
from lib.tag import *
from lib import DBAccess
from lib.user import User

class AdminPage(Page):
    """
    管理画面出力
    """
    def __init__(self, session, setting, form_data=None):
        super(AdminPage, self).__init__(session, setting, form_data)
        self.set_title(u'管理画面')
        self.dba = DBAccess.order()
    def make_page(self):
        """
        ページの処理
        """
        mode = self.form_data.getvalue('mode')
        username = self.form_data.getvalue('username')
        password = self.form_data.getvalue('password')
        login = self.session.getvalue('admin', False)
        enable = self.setting['admin']['enable'] == 'On'
        users = []
        login_faled = False

        if enable:
            if mode == 'login':
                if username == self.setting['admin']['user']  and  password == self.setting['admin']['pass']:
                    self.session.setvalue('admin', True)
                    login = True
                else:
                    login_faled = True
            elif mode == 'logout':
                self.session.delvalue('admin')
                login = False
            elif mode == 'reset_password':
                user = User(username)
                user.reset_password(new_password=password, salt=self.setting['password']['salt'], force=True)
                user.update()
        if login:
            users = self.dba.select('user_tbl', '*')

        # テンプレ―ト用データ
        template_data = {}
        template_data['enable'] = enable
        template_data['login'] = login
        template_data['login_failed'] = login_faled
        template_data['users'] = users

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'管理画面'))
        if not data['enable']:
            page.add_value(PTag(u'アクセス許可がありません'))
        elif not data['login']:
            page.add_value([
                FormTag(action='./admin', values=[
                    TableTag([
                        TRTag([TDTag(u'ユーザ名'), TDTag(':'), TDTag('%s' % TextTag(name='username', value=''))]),
                        TRTag([TDTag(u'パスワード'), TDTag(':'), TDTag('%s' % PasswordTag(name='password', value=''))]),
                    ]),
                    HiddenTag(name='mode', value='login'),
                    SubmitTag(value=u'ログイン'),
                ])
            ])
            if data['login_failed']:
                page.add_value(PTag(u'ログインに失敗しました'))
        else:
            page.add_value([
                FormTag(action='./admin', values=[
                    HiddenTag(name='mode', value='logout'),
                    SubmitTag(value=u'ログアウト'),
                ])
            ])
            # user_tbl
            user_tbl = TableTag(caption=u'user_tbl', elements={'border':3})
            tr = TRTag(elements={'bgcolor':'gray'})
            user_tbl_fields = ['user_id', 'username', 'nickname', 'hash', 'password', 'login_time', 'create_time']
            for field in user_tbl_fields:
                tr.add_value(TDTag(str(field)))
            tr.add_value([
                TDTag(' '),
                TDTag(u'パスワードリセット'),
            ])
            user_tbl.add_value(tr)
            for user in data['users']:
                tr = TRTag()
                for field in user_tbl_fields:
                    tr.add_value(TDTag(escape(u'%s'%user[field])))
                tr.add_value([
                    TDTag(' '),
                    FormTag(action='./admin', values=TDTag([TextTag('password'),HiddenTag('mode','reset_password'),HiddenTag('username',user['username']),SubmitTag(value=u'リセット')]))
                ])
                user_tbl.add_value(tr)
            page.add_value(user_tbl)


        return page


if __name__ == '__main__':
    pass
