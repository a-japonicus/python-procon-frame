#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        top
# Purpose:     トップ画面
#
# Author:      hatahata
#
# Created:     08/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import hashlib
from page import Page
from lib.session.session import Session
from lib.tag import *
from lib.db_access import DBAccess

class TopPage(Page):
    """
    トップページ出力
    """
    def __init__(self, session, setting, form_data=None):
        super(TopPage, self).__init__(session, setting, form_data)
        self.set_title(u'トップ')
        self.set_session(session)
        self.dba = DBAccess(setting['database'])
    def make_page(self):
        """
        ページの処理
        """
        # テンプレ―ト用データ
        template_data = {}

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = DivTag('page', [
            H2Tag(u'トップ画面'),
            DivTag('update', [
            H3Tag(u'更新履歴'),
                TableTag(elements = {'border':2, 'rules':'none'}, values=[
                    TRTag([TDTag(u'2012/01/08'), TDTag('<br>'), TDTag(u'トップ画面作成')]),
                    TRTag([TDTag(u'2012/01/07'), TDTag('<br>'), TDTag(u'登録画面作成')]),
                    TRTag([TDTag(u'2012/01/07'), TDTag('<br>'), TDTag(u'ログアウト画面作成')]),
                    TRTag([TDTag(u'2011/12/31'), TDTag('<br>'), TDTag(u'ログイン画面作成')]),
                    TRTag([TDTag(u'2011/12/31'), TDTag('<br>'), TDTag(u'フレーム作成')]),
                    ]
                )
            ])
        ])

        return page


if __name__ == '__main__':
    pass
