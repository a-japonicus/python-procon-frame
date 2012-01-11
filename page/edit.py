#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        edit
# Purpose:     問題作成画面
#
# Author:      hatahata
#
# Created:     09/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
from xml.sax.saxutils import *
from page import Page
from lib.tag import *
from lib import DBAccess
from lib.user import User

class EditPage(Page):
    """
    問題作成ページ出力
    """
    def __init__(self, session, setting, form_data=None):
        super(EditPage, self).__init__(session, setting, form_data)
        self.set_title(u'問題作成')
        self.set_session(session)
        self.dba = DBAccess.order()
    def make_page(self):
        """
        ページの処理
        """
        login = self.session.getvalue('login', False)
        mode = self.form_data.getvalue('mode')
        title = unicode(self.form_data.getvalue('title', '練習問題'), 'utf-8')
        data = unicode(self.form_data.getvalue('data', 'ここに問題文を入力してください'), 'utf-8')
        
        if mode == 'regist':
            if self.form_data.getvalue('return') is not None:
                mode = ''
            else:
                # 問題登録
                # TODO:問題の整合性チェック
                user = User(self.session.getvalue('username'))
                title = unicode(self.form_data.getvalue('title', ''), 'utf-8')
                data = unicode(self.form_data.getvalue('data', ''), 'utf-8')
                user_id = user.getvalue('user_id', -1)
                if title is not None and data is not None and user_id is not None:
                    self.dba.insert('problem_tbl', {'user_id':user_id, 'title':title, 'data':data})
        
        # テンプレ―ト用データ
        template_data = {}
        template_data['login'] = login
        template_data['mode'] = mode
        template_data['problem_title'] = title
        template_data['problem_data'] = data

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'問題作成'))

        if not data['login']:
            page.add_value(PTag(u'問題を登録するには%sする必要があります。'%ATag('./login',u'ログイン')))
        elif data['mode'] == 'upload':
            page.add_value([
                PTag(u'この内容で登録してもよろしいですか？'),
                FormTag(action='./edit', values=[
                    u'問題名：%s'%TextTag(name='title', value=escape(data['problem_title']), elements={'readonly':None}),BRTag(),
                    TextAreaTag(name='data', values=escape(data['problem_data']), elements={'cols':100, 'rows':20, 'readonly':None}),BRTag(),
                    HiddenTag(name='mode', value='regist'),
                    SubmitTag(name='return', value=u'戻る'),
                    SubmitTag(name='regist', value=u'登録'),
                ])
            ])
        elif data['mode'] == 'regist':
            page.add_value(PTag(u'問題を登録しました'))
#            page.add_value(PTag(str(self.dba.select('problem_tbl'))))
#            page.add_value(PTag(data['problem_title']))
#            page.add_value(PTag(data['problem_data']))
        else:
            page.add_value(
                FormTag(action='./edit', values=[
                    u'問題名：%s'%TextTag(name='title', value=escape(data['problem_title'])),BRTag(),
                    TextAreaTag(name='data', values=escape(data['problem_data']), elements={'cols':100, 'rows':20}),BRTag(),
                    HiddenTag(name='mode', value='upload'),
                    SubmitTag(value=u'決定'),
                ])
            )
            
        return page


if __name__ == '__main__':
    pass
