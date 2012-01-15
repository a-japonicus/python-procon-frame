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
        login =  self.session.getvalue('login', False)
        self.session.delvalue('login')
        self.session.delvalue('user_id')
#        self.session.delete()

        # ログアウトしたらトップ画面を表示
        if login:
            from top import TopPage
            top = TopPage(self.request)
            return top.index(param)

        # テンプレ―ト用データ
        template_data = {}

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', [
            H2Tag(u'ログアウト画面'),
            PTag(u'ログインしていません')
        ])
        return self.html_page_template(page)


if __name__ == '__main__':
    pass
