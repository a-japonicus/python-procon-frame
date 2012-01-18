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
from xml.sax.saxutils import *
from page import Page
from lib.tag import *
from lib import DBAccess
from lib.user import User
from lib.problem import *

class TopPage(Page):
    """
    トップページ出力
    """
    def __init__(self,request):
        self.request = request
        self.session = request['Session']
        self.form_data = request['Post']
        self.set_title(u'トップ')
        self.dba = DBAccess.order()
    def index(self, param):
        """
        ページの処理
        """
        probs = get_problems()
        users = {}
        for p in probs:
            user_id = p.getvalue('user_id', None)
            if user_id and not user_id in users.keys():
                users[user_id] = User(user_id)


        # テンプレ―ト用データ
        template_data = {}
        template_data['problems'] = probs
        template_data['users'] = users

        return self.template(template_data)

    def template(self, data):
        """
        なんちゃってテンプレート
        """
        page = CenterTag([
            H2Tag(u'トップ画面'),
            DivTag('update', [
                TableTag(caption=u'更新履歴',elements = {'border':2, 'rules':'none'}, values=[
                    TRTag([TDTag(u'2012/01/16'), TDTag(':'), TDTag(u'問題画面追加')]),
                    TRTag([TDTag(u'2012/01/09'), TDTag(':'), TDTag(u'問題作成画面追加')]),
                    TRTag([TDTag(u'2012/01/09'), TDTag(':'), TDTag(u'プロフィール画面追加')]),
                    TRTag([TDTag(u'2012/01/08'), TDTag(':'), TDTag(u'管理画面追加')]),
                    TRTag([TDTag(u'2012/01/08'), TDTag(':'), TDTag(u'トップ画面追加')]),
                    TRTag([TDTag(u'2012/01/07'), TDTag(':'), TDTag(u'登録画面追加')]),
                    TRTag([TDTag(u'2012/01/07'), TDTag(':'), TDTag(u'ログアウト画面追加')]),
                    TRTag([TDTag(u'2011/12/31'), TDTag(':'), TDTag(u'ログイン画面追加')]),
                    TRTag([TDTag(u'2011/12/31'), TDTag(':'), TDTag(u'フレーム追加')]),
                    ]
                )
            ])
        ])

        page.add_value('<br><br>')

        prob_table = TableTag(u'問題',TRTag([
                                TDTag(u'問題番号'),
                                TDTag(u'問題名'),
                                TDTag(u'投稿者'),
                        ]),{'border':'2'})
        for p in data['problems']:
            prob_table.add_value(TRTag([
                TDTag(u'%d'%p.getvalue('problem_id','-1')),
                TDTag(ATag('/problem/index/%d'%p.getvalue('problem_id',-1), p.getvalue('title',''))),
                TDTag(data['users'][p.getvalue('user_id',-1)].getvalue('nickname','')),
            ]))
        page.add_value(prob_table)

        return self.html_page_template(DivTag('page', page))


if __name__ == '__main__':
    pass
