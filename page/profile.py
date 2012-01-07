#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        profile
# Purpose:     プロフィール画面
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

class ProfilePage(Page):
    """
    プロフィールページ出力
    """
    def __init__(self, session, setting, form_data=None):
        super(ProfilePage, self).__init__(session, setting, form_data)
        self.set_title(u'プロフィール')
        self.set_session(session)
        self.dba = DBAccess(setting['database'])
    def make_page(self):
        """
        ページの処理
        """
        login = self.session.getvalue('login', False)
        username = self.session.getvalue('username', '')
        userid = ''
        nickname = ''
        userhash = ''

        if login:
            userdata = self.dba.select(table='user_tbl', fields='*', where={'username':username}, limit=1)
            if len(userdata) == 1:
                userid = str(userdata[0]['user_id'])
                nickname = userdata[0]['nickname']
                userhash = userdata[0]['hash']
            else:
                login = False


        # テンプレ―ト用データ
        template_data = {}
        template_data['login'] = login
        template_data['userid'] = userid
        template_data['username'] = username
        template_data['nickname'] = nickname
        template_data['userhash'] = userhash
        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'プロフィール画面'))
        if not data['login']:
            page.add_value(PTag(u'ログインしていません'))
        else:
            page.add_value(
                TableTag([
                    TRTag([TDTag(u'ユーザID'), TDTag(data['userid'])]),
                    TRTag([TDTag(u'ユーザ名'), TDTag(data['username'])]),
                    TRTag([TDTag(u'ニックネーム'), TDTag(data['nickname'])]),
                    TRTag([TDTag(u'ハッシュ'), TDTag(data['userhash'])]),
                ])
            )

        return page


if __name__ == '__main__':
    pass
