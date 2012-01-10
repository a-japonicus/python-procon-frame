#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        index
# Purpose:
#
# Author:      hatahata
#
# Created:     31/12/2011
# Copyright:   (c) hatahata 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import os
from xml.sax.saxutils import *
from lib.response import BaseResponse
from lib.session import Session
from lib.tag import *
from lib import DBAccess

class AppResponse(BaseResponse):
    def __init__(self, request, charset='utf-8'):
        super(AppResponse, self).__init__(request.get('Cookie'), charset)
        self.request = request
        self.error_info = []
        self.title=''
        self.make_html()
    def make_top(self):
        #トップ部分作成
        session = self.request.get('Session')
        top = DivTag('top')
        top.add_value(H1Tag(u'テストページ'))
        if session.getvalue('login', False):
            top.add_value(PTag(u'ログイン中です'))
        top_links = [('top', u'トップ'), ('edit', u'問題作成'), ('bbs', u'掲示板'), ('about', u'取扱説明書'), ('profile', u'プロフィール'), ('regist', u'登録'), ('logout', u'ログアウト'), ('login', u'ログイン'), ('admin', u'管理画面')]
        for p in top_links:
        #    if page != p[0]:
                top.add_value(u'[%s]' % ATag('./%s'%p[0], p[1]))
        #    else:
        #        top.add_value(u'[%s]' % p[1])
        return top
    def make_page(self):        
        route = self.request.get('Route')
        session = self.request.get('Session')
        setting = self.request.get('Setting')
        post = self.request.get('Post')

        if len(route) == 0:
            route = ['top']

        page = route[0]
        # ページクラスを取得
        response_page = None
        try:
            # ページクラスを動的インポート
            page_class_name = page.capitalize()+'Page'
            page_class = getattr(__import__('page.'+page, {}, {}, page_class_name), page_class_name)
            response_page = page_class(session, setting, post)
            page_data = response_page.make_page()
        except:
            import sys
            self.error_info.append(sys.exc_info())
            response_page = None
        
        # ページクラスが読み込めなければ未実装と判定
        if response_page is None:
            from page.page import Page
            response_page = Page(session, setting, post)
            page_data = response_page.make_page()
        self.title = response_page.get_title()
        return page_data
    def make_html(self):
        # デバッグ出力
        debug_output = ""
        setting = self.request.get('Setting')
        if setting['debug']['enable'] == 'On':
            debug_output = DivTag('debug',[BRTag(),BRTag(),H3Tag(u'デバッグ')])
            for info in self.error_info:
                debug_output.add_value(PTag(escape(str(info))))
            """
            for flist in form.list:
                print (escape(str(flist)).encode('utf-8'))
                print('<br>')
            """
        #    for k,v in os.environ.items():
        #        print (k,v)
        
        # HTMLの組立て
        self.add_response_data(
            HtmlTag([
                HeadTag(TitleTag(u'テストページ[%s]' % escape(self.title))),
                BodyTag([
                    CenterTag([
                        self.make_top(),
                        HRTag(),
                        self.make_page(),
                        debug_output,
                    ])
                ])
            ])
        )
"""
session.close()
if session.exist():
    # クッキーにセッションIDをセット
    response.set_cookie(setting['session']['id'], session.get_session_id(), session.get_lifetime())
else:
    # セッションが存在しないのでクッキー削除
    response.set_cookie(setting['session']['id'], '', -1)
#print (response)

"""
