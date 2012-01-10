#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Session
# Purpose:     セッション管理クラス
#
# Author:      hatahata
#
# Created:     03/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import os
import pickle
import json
import uuid
import hashlib
import random

# ガーベジコレクション確率
GC_PROB = 0.05

_instance = None
def create(setting, session_id=None):
    global _instance
    if _instance == None:
        _instance = Session(setting, session_id)
    return _instance
def order():
    global _instance
    return _instance

class Session(object):
    """
    セッション管理クラス
    """
    def __init__(self, setting, session_id=None):
        self.setting = setting
        self.serializer = pickle
        self.session_id = session_id
        self.prev_session_id = []
        self.lifetime = int(self.setting['lifetime'], 10)
        self.create_handler()
        if self.session_id is not None:
            self.load()
        else:
            self.data = {}
        self.regenerate_id()
        if random.random() <= GC_PROB:
            self.handler.gc(self.lifetime)
    def create_handler(self):
        """
        ハンドラ生成
        """
        handler = None
        if self.setting['handler'] == 'file':
            from lib.session.FileSessionHandler import FileSessionHandler
            handler = FileSessionHandler(self.setting)
        elif self.setting['handler'] == 'database':
            from lib.session.DBSessionHandler import DBSessionHandler
            handler = DBSessionHandler(self.setting)
        handler.open()
        self.handler = handler
    def load(self):
        """
        セッション読み込み
        """
        data = self.handler.read(self.session_id, self.lifetime)
        try:
            self.data = self.serializer.loads(data)
        except:
            self.regenerate_id()
            self.data = {}
    def save(self):
        """
        セッション保存
        """
        if self.session_id is None:
            self.regenerate_id()
        if self.session_id is not None:
            self.handler.write(self.session_id, self.serializer.dumps(self.data))
#            data = self.handler.read(self.session_id)
#            print(self.data, self.serializer.loads(data.encode('utf-8')))
#            raise Exception(self.serializer.dumps(self.data), self.serializer.loads(data.encode('utf-8')))
    def delete(self):
        """
        セッション削除
        """
        self.handler.delete(self.session_id)
        self.session_id = None
    def setvalue(self, key, value):
        """
        セッションに値書き込み
        """
        self.data[key] = value
    def getvalue(self, key, default=None):
        """
        セッションから値取得
        """
        if key in self.data:
            return self.data[key]
        return default
    def regenerate_id(self):
        """
        セッションID再生成
        """
        for i in range(10):
            session_id = hashlib.md5('%s' % uuid.uuid4()).hexdigest()
            if self.handler.create(session_id):
                break
            else:
                session_id = None
        if session_id is not None:
            self.prev_session_id.append(self.session_id)
            self.session_id = session_id
    def get_lifetime(self):
        return self.lifetime
    def get_session_id(self):
        """
        セッションID取得
        """
        return self.session_id
    def exist(self):
        if self.session_id is None:
            return False
        return True
    def close(self):
        """
        セッションクローズ
        """
        if self.session_id is not None:
            self.save()

        # 過去のセッションIDを削除
        for prev_id in self.prev_session_id:
            self.handler.delete(prev_id)
        self.handler.close()
