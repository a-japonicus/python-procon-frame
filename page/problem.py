#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        problem
# Purpose:     問題ページ
#
# Author:      hatahata
#
# Created:     16/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import hashlib
from xml.sax.saxutils import *
from page import Page
from lib.tag import *
from lib import DBAccess
from lib.user import User,get_user_by_hash
from lib.problem import *

class ProblemPage(Page):
    """
    問題ページ出力
    """
    def __init__(self,request):
        self.request = request
        self.session = request['Session']
        self.form_data = request['Post']
        self.set_title(u'問題')
        self.dba = DBAccess.order()
    def index(self, param):
        """
        ページの処理
        """
        print(param)
        if len(param) > 0:
            prob = Problem(param[0])
            if prob.correct():
                template_data={}
                template_data['id'] = prob.getvalue('problem_id', -1)
                template_data['title'] = prob.getvalue('title', '')
                template_data['data'] = prob.getvalue('data', '')
                print(template_data['data'])
                return self.problem_template(template_data)

        template_data = {}
        template_data['problem_id'] = -1

        return self.missing_template(template_data)

    def get(self, param):
        """
        問題取得（テキスト）
        """
        print(param)
        if len(param) > 0:
            prob = Problem(param[0])
            if prob.correct():
                return prob['data']

        return None

    def send(self, param):
        """
        回答受信
        """
        recv = u'回答を受信しました\r\n'
        key = self.form_data.getvalue('key')
        data = self.form_data.getvalue('file')
        if key is not None:
            user = get_user_by_hash(key)
            if user:
                recv += u'ユーザ名:%s\r\n' % user['username']
            else:
                recv += u'ユーザが見つかりません。ハッシュを確認してください。\r\n'
        recv += u'受信データサイズ:%d\r\n' % len(data)

        return recv

    def problem_template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'問題%d[%s]' %(data['id'], escape(data['title']))))
        page.add_value(TextAreaTag('data', escape(data['data']), {'cols':100, 'rows':20, 'readonly':None}))

        return self.html_page_template(page)

    def missing_template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'問題が見つかりません'))

        return self.html_page_template(page)

if __name__ == '__main__':
    pass
