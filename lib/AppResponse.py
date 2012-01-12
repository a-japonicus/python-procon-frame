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
from xml.sax.saxutils import *
from lib.response import BaseResponse
from lib.tag import *
from lib.user import User

class AppResponse(BaseResponse):
    """
    アプリケーションのレスポンス
    """
    def __init__(self, request, charset='utf-8'):
        super(AppResponse, self).__init__(request.get('Cookie'), charset)
        self.request = request
        self.error_info = []
        self.title=''
        self.make_html()

    def make_page(self):
        """
        メインのページ部分作成
        """
        route = self.request.get('Route')
        session = self.request.get('Session')
        setting = self.request.get('Setting')
        post = self.request.get('Post')

        if route[0] == '':
            route = ['top']

        page = route[0]
        # ページクラスを取得
        response_page = None
        try:
            # ページクラスを動的インポート
            page_class_name = page.capitalize()+'Page'
            page_class = getattr(__import__('page.'+page, {}, {}, page_class_name), page_class_name)
            response_page = page_class(session, setting, post)
            page_data = response_page.make_html()
        except:
            import sys
            self.error_info.append(sys.exc_info())
            response_page = None

        # ページクラスが読み込めなければ未実装と判定
        if response_page is None:
            from page.page import Page
            response_page = Page(session, setting, post)
            page_data = response_page.make_html()

        self.title = response_page.get_title()

        return page_data

    def make_html(self):
        """
        HTMLの組立
        """
        try:
            page = self.make_page()
        except:
            import sys
            self.error_info.append(sys.exc_info())

        # デバッグ出力
        debug_output = ""
        setting = self.request.get('Setting')
        if setting['debug']['enable'] == 'On':
            debug_output = DivTag('debug',Tag('font', H3Tag(u'デバッグモード'), {'color':'red'}))
            # SESSION
            session_items = self.request.get('Session').items()
            if len(session_items) > 0:
                session_list = PTag(Tag('font', Tag('b','SESSION: '), {'size':3}))
                for name,value in session_items:
                    session_list.add_value(escape(unicode('%s => %s, ' % (name, value), 'utf-8')))
                debug_output.add_value(session_list)
            # POST
            post_list = PTag(Tag('font', Tag('b','POST: '), {'size':3}))
            post = self.request.get('Post')
            post_items = post.items()
            if len(post_items) > 0:
                for name,value in post_items:
                    post_list.add_value(escape(unicode('%s => %s, ' % (name, value), 'utf-8')))
                debug_output.add_value(post_list)
            # ERROR
            if len(self.error_info) > 0:
                error_list = PTag(Tag('font', Tag('b','ERROR: '), {'size':3}))
                for info in self.error_info:
                    error_list.add_value(escape('%s, ' % str(info)))
                debug_output.add_value(error_list)

            self.add_response_data(CenterTag(debug_output))

        # HTMLの組立て
        self.add_response_data(page)

