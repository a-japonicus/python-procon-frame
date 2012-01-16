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
from xml.sax.saxutils import *
from page import Page
from lib.tag import *

class LogoutPage(Page):
    """
    ログアウトページ出力
    """
    def __init__(self,request):
        self.request = request
        self.session = request['Session']
        self.form_data = request['Post']
        self.set_title(u'ログアウト')
    def index(self, param):
        """
        ページの処理
        """
        logout = False
        login = self.session.getvalue('login', False)
        if login:
            self.session.delvalue('login')
            self.session.delvalue('user_id')
            logout = True
#        self.session.delete()

        # テンプレ―ト用データ
        template_data = {}
        template_data['logout'] = logout

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        if data['logout']:
            return self.redirect('/top')
        page = DivTag('page', [
            H2Tag(u'ログアウト画面'),
            PTag(u'ログインしていません')
        ])
        return self.html_page_template(page)


if __name__ == '__main__':
    pass
