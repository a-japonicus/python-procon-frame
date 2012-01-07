#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        logout
# Purpose:     ログアウトページ
#
# Author:      hatahata
#
# Created:     07/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
from page import Page
from session import Session
from tag import *

class LogoutPage(Page):
    """
    ログアウトページ出力
    """
    def __init__(self, session, setting, form_data=None):
        super(LogoutPage, self).__init__(session, setting, form_data)
        self.set_title(u'ログアウト')
        self.set_session(session)

    def make_page(self):
        """
        ページの処理
        """
        login =  self.session.getvalue('login', False)
        self.session.setvalue('login', False)

        # テンプレ―ト用データ
        template_data = {}
        template_data['login'] = login

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'ログアウト画面'))
        if not data['login']:
            page.add_value(PTag(u'ログインしていません'))
        else:
            page.add_value(PTag(u'ログアウトしました'))

        return page


if __name__ == '__main__':
    pass
