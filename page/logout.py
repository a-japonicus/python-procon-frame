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
    def __init__(self, session, setting, form_data=None):
        super(LogoutPage, self).__init__(session, setting, form_data)
        self.set_title(u'ログアウト')
    def make_page(self):
        """
        ページの処理
        """
        login =  self.session.getvalue('login', False)
        self.session.delvalue('login')
        self.session.delvalue('user_id')
#        self.session.delete()

        # テンプレ―ト用データ
        template_data = {}
        template_data['login'] = login

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = ''
        if not data['login']:
            page = DivTag('page', [
                H2Tag(u'ログアウト画面'),
                PTag(u'ログインしていません')
            ])
        else:
            from top import TopPage
            top = TopPage(self.session, self.setting, self.form_data)
            page = top.make_page()
        return page


if __name__ == '__main__':
    pass
