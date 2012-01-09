#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        profile
# Purpose:     プロフィール画面
#
# Author:      hatahata
#
# Created:     08/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import hashlib
import uuid
from xml.sax.saxutils import *
from page import Page
from lib.session.session import Session
from lib.tag import *
from lib import DBAccess
from lib.user import User

EDIT_NONE = 0
EDIT_CORRECT = 1
EDIT_FAILED = 2

class ProfilePage(Page):
    """
    プロフィールページ出力
    """
    def __init__(self, session, setting, form_data=None):
        super(ProfilePage, self).__init__(session, setting, form_data)
        self.set_title(u'プロフィール')
        self.set_session(session)
        self.dba = DBAccess.order()
    def update_password(self, username, old_password, new_password):
        pass
    def make_page(self):
        """
        ページの処理
        """
        login = self.session.getvalue('login', False)
        username = self.session.getvalue('username', '')
        mode = self.form_data.getvalue('mode')
        reset_hash = self.form_data.getvalue('reset_hash', '') == 'reset'
        nickname = unicode(self.form_data.getvalue('nickname', ''), 'utf-8')
        edit_status = EDIT_NONE
        userid = ''
        userhash = ''
        
        user = User(username)
        if login:
            if mode == 'pass_update':
                old_password = self.form_data.getvalue('old_password', '')
                new_password = self.form_data.getvalue('new_password', '')
                retype_password = self.form_data.getvalue('retype_password', '')
                if new_password == retype_password:
                    if user.reset_password(old_password, new_password, self.setting['password']['salt']):
                        edit_status = EDIT_CORRECT
                    else:
                        edit_status = EDIT_FAILED
            elif mode == 'update':
                if reset_hash:
                    user.reset_hash()
                if nickname != '':
                    user.setvalue('nickname', nickname)
                edit_status = EDIT_CORRECT
            user.update()

        # テンプレ―ト用データ
        template_data = {}
        template_data['login'] = login
        template_data['userid'] = str(user.getvalue('user_id', -1))
        template_data['username'] = user.getvalue('username', '')
        template_data['nickname'] = user.getvalue('nickname', '')
        template_data['userhash'] = user.getvalue('hash', '')
        template_data['mode'] = mode
        template_data['edit_status'] = edit_status
        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', H2Tag(u'プロフィール画面'))
        if not data['login']:
            page.add_value(PTag(u'ログインしていません'))
        elif data['mode'] == 'edit':
            page.add_value([
                FormTag(action='./index.py?page=profile', values=[
                    TableTag([
                        TRTag([TDTag(u'ユーザID'), TDTag(':'), TDTag(data['userid'])]),
                        TRTag([TDTag(u'ユーザ名'), TDTag(':'), TDTag(data['username'])]),
                        TRTag([TDTag(u'ニックネーム'), TDTag(':'), TDTag(TextTag('nickname', data['nickname']))]),
                        TRTag([TDTag(u'ハッシュ'), TDTag(':'), TDTag(data['userhash']), TDTag(u'%sリセット' % CheckBoxTag('reset_hash', 'reset'))]),
                    ]),
                    HiddenTag('mode', 'update'),
                    SubmitTag(value=u'更新'),
                ]),
            ])
        elif data['mode'] == 'pass_edit':
            page.add_value([
                FormTag(action='./index.py?page=profile', values=[
                    TableTag([
                        TRTag([TDTag(u'旧パスワード'), TDTag(':'), TDTag(PasswordTag('old_password', ''))]),
                        TRTag([TDTag(u'新パスワード'), TDTag(':'), TDTag(PasswordTag('new_password', ''))]),
                        TRTag([TDTag(u'新パスワード（確認用）'), TDTag(':'), TDTag(PasswordTag('retype_password', ''))]),
                    ]),
                    HiddenTag('mode', 'pass_update'),
                    SubmitTag(value=u'更新'),
                ]),
            ])
        else:
            page.add_value([
                TableTag([
                    TRTag([TDTag(u'ユーザID'), TDTag(':'), TDTag(escape(data['userid']))]),
                    TRTag([TDTag(u'ユーザ名'), TDTag(':'), TDTag(escape(data['username']))]),
                    TRTag([TDTag(u'ニックネーム'), TDTag(':'), TDTag(escape(data['nickname']))]),
                    TRTag([TDTag(u'ハッシュ'), TDTag(':'), TDTag(escape(data['userhash']))]),
                ]),
                TableTag(TRTag([
                    FormTag(action='./index.py?page=profile', values=[
                        HiddenTag('mode', 'edit'),
                        SubmitTag(value=u'編集'),
                    ]),
                    FormTag(action='./index.py?page=profile', values=[
                        HiddenTag('mode', 'pass_edit'),
                        SubmitTag(value=u'パスワード変更'),
                    ])])
                ),
            ])
            if data['edit_status'] == EDIT_CORRECT:
                page.add_value(PTag(u'更新しました'))
            elif data['edit_status'] == EDIT_FAILED:
                page.add_value(PTag(u'更新に失敗しました'))

        return page


if __name__ == '__main__':
    pass
