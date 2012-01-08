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
from page import Page
from lib.session.session import Session
from lib.tag import *
from lib.db_access import DBAccess

class AdminPage(Page):
    """
    管理画面出力
    """
    def __init__(self, session, setting, form_data=None):
        super(AdminPage, self).__init__(session, setting, form_data)
        self.set_title(u'管理画面')
        self.set_session(session)
        self.dba = DBAccess(setting['database'])
    def make_page(self):
        """
        ページの処理
        """
        mode = self.form_data.getvalue('mode')
        username = self.form_data.getvalue('username')
        password = self.form_data.getvalue('password')
        login = self.session.getvalue('admin', False)
        enable = self.setting['admin']['enable'] == 'On'
        user_tbl = []
        login_faled = False

        if enable:
            if mode == 'login':
                if username == self.setting['admin']['user']  and  password == self.setting['admin']['pass']:
                    self.session.setvalue('admin', True)
                    login = True
                else:
                    login_faled = True
            elif mode == 'logout':
                self.session.setvalue('admin', False)
                login = False
        if login:
            user_tbl = self.dba.select('user_tbl', '*')

        # テンプレ―ト用データ
        template_data = {}
        template_data['enable'] = enable
        template_data['login'] = login
        template_data['login_failed'] = login_faled
        template_data['user_tbl'] = user_tbl

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
                FormTag(action='./index.py?page=admin', values=[
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
                FormTag(action='./index.py?page=admin', values=[
                    HiddenTag(name='mode', value='logout'),
                    SubmitTag(value=u'ログアウト'),
#                    ATag('./index.py?page=admin', u'ログアウト')
                ])
            ])
            # user_tbl
            user_tbl = TableTag(caption=u'user_tbl', elements={'border':3})
            tr = TRTag(elements={'bgcolor':'gray'})
            for k,v in data['user_tbl'][0].items():
                tr.add_value(TDTag(u'%s'%k))
            user_tbl.add_value(tr)
            for user in data['user_tbl']:
                tr = TRTag()
                for k,v in user.items():
                    tr.add_value(TDTag(u'%s'%v))
                user_tbl.add_value(tr)
            page.add_value(user_tbl)


        return page


if __name__ == '__main__':
    pass
