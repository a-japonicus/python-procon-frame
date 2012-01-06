#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        SessionHandler
# Purpose:     セッションハンドラ基本クラス
#
# Author:      hatahata
#
# Created:     03/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import uuid
import random

#ガーベジコレクションの確率
GC_PROB = 0.05

class SessionHandler(object):
    """
    セッションハンドラ基本クラス
    """
    def __init__(self):
        pass
    def create(self, session_id):
        """
        セッション生成
        """
        return False
    def read(self, session_id, session_limit):
        """
        セッション読み込み
        """
        return {}
    def write(self, session_id, data):
        """
        セッション書き込み
        """
        pass
    def delete(self, session_id):
        """
        セッション削除
        """
        pass
    def open(self):
        """
        セッション開始
        """
        pass
    def close(self):
        """
        セッション終了
        """
        pass
    def gc(self):
        """
        ガーベジコレクション
        """
        pass

if __name__ == '__main__':
    pass
