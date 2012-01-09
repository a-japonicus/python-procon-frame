#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        page
# Purpose:     ページクラス
#
# Author:      hatahata
#
# Created:     03/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
from lib.tag import *
from lib.session.session import Session

class Page(object):
    """
    ページクラス
    """
    def __init__(self, session, setting, form_data=None):
        self.set_title(u'未実装ページ')
        self.setting = setting
        if form_data is None:
            import cgi
            self.form_data = cgi.FieldStorage()
        else:
            self.form_data = form_data
    def set_session(self, session):
        self.session = session
    def get_title(self):
        return self.title
    def set_title(self, title):
        self.title = title
    def make_page(self):
        """
        ページの処理
        """
        return self.template(data={})
    def template(self, data):
        """
        なんちゃってテンプレート
        """
        return DivTag('page', PTag(u'未実装ページです'))
    def __str__(self):
        return '%s' % self.make_page();


if __name__ == '__main__':
    page = Page()
    print('%s'.encode('utf-8') % page)
