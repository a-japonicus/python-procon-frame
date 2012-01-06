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
from tag import *
from session import Session

class Page(object):
    """
    ページクラス
    """
    def __init__(self, title=u'未実装ページ', form_data=None):
        self.set_title(title)
        if form_data == None:
            import cgi
            self.form_data = cgi.FieldStorage()
        else:
            self.form_data = form_data
        self.page = DivTag('page')
    def set_session(self, session):
        self.session = session
    def get_title(self):
        return self.title
    def set_title(self, title):
        self.title = title
    def make_page(self):
        return self.template(data={})
    def template(self, data):
        page = DivTag('page')
        page.add_value(u'未実装ページです')
        return page
    def __str__(self):
        return '%s' % self.make_page_data();


if __name__ == '__main__':
    page = Page()
    print('%s'.encode('utf-8') % page)
