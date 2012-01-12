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
from xml.sax.saxutils import *
from lib.tag import *
from lib.user import User

class Page(object):
    """
    ページクラス
    """
    def __init__(self, session, setting, form_data=None):
        self.set_title(u'未実装ページ')
        self.contetn_types = []
        self.session = session
        self.setting = setting
        if form_data is None:
            import cgi
            self.form_data = cgi.FieldStorage()
        else:
            self.form_data = form_data
        self.contenttype_html()
    def get_title(self):
        return self.title
    def set_title(self, title):
        self.title = title
    def set_contenttype(self, contenttype):
        self.contetn_type = contenttype
    def contenttype_html(self):
        """
        HTML出力
        デフォルトではこれ
        """
        self.set_contenttype('text/html')
    def contenttype_txt(self):
        """
        テキストの出力
        """
        self.set_contenttype('text/plane')
    def make_top(self):
        """
        トップ部分作成
        """
        top = DivTag('top', H1Tag(u'テストページ'))
        if self.session.getvalue('login', False):
            user_id = self.session.getvalue('user_id')
            user = User(user_id)
            top.add_value(PTag(u'ログイン中です:[%s] %s さん' % (escape(user.getvalue('username','')), escape(user.getvalue('nickname', '')))))
        top_links = [('top', u'トップ'), ('edit', u'問題作成'), ('bbs', u'掲示板'), ('about', u'取扱説明書'), ('profile', u'プロフィール'), ('regist', u'登録'), ('logout', u'ログアウト'), ('login', u'ログイン'), ('admin', u'管理画面')]
        for p in top_links:
            top.add_value(u'[%s]' % ATag('./%s'%p[0], p[1]))

        return top
    def make_page(self):
        """
        ページ部分の作成
        基本的にはここを書き換える
        """
        return DivTag('page', PTag(u'未実装ページです'))
    def html_page_template(self, page):
        """
        HTMLのテンプレ―ト
        """
        html = HtmlTag([
                HeadTag(TitleTag(u'テストページ[%s]' % escape(self.get_title()))),
                BodyTag([
                    CenterTag([
                        self.make_top(),
                        HRTag(),
                        self.make_page(),
                    ])
                ])
            ])
        return html
    def make_html(self):
        """
        HTMLの作成
        """
        return self.html_page_template(self.make_page())
    def __str__(self):
        return '%s' % self.make_html();


if __name__ == '__main__':
    page = Page()
    print('%s'.encode('utf-8') % page)
