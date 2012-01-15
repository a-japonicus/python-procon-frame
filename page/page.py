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
    def __init__(self, request):
        self.set_title(u'未実装ページ')
        self.request = request
        self.contetn_types = []
        self.session = request['Session']
        self.form_data = request['Post']
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
    def error(self, param):
        """
        エラーページ
        """
        html = HtmlTag([
                HeadTag(TitleTag(u'テストページ[未実装ページです]')),
                BodyTag([
                    CenterTag([
                        self.make_top(),
                        HRTag(),
                        DivTag('page', PTag(u'未実装ページです')),
                    ])
                ])
            ])
        return html
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
                        page,
                    ])
                ])
            ])
        return html


if __name__ == '__main__':
    page = Page()
    print('%s'.encode('utf-8') % page)
