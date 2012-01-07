#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Session
# Purpose:     セッション管理クラス
#              セッションアダプションがあるので、ログイン時にregenerate_id()を呼ぶのを忘れずに
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
import time
import datetime
import copy
import hashlib
from Cookie import SimpleCookie
import random

# ガーベジコレクション確率
GC_PROB = 0.05
# クッキー内のセッションID名
COOKIE_SESSIONID = 'SESSIONID'

class Session(object):
    """
    セッション管理クラス
    """
    def __init__(self, cookie, handler, setting):
        self.cookie = cookie
        self.setting = setting
        self.handler = handler
        self.serializer = pickle
        self.session_id = None
        self.prev_session_id = []
        self.lifetime = int(self.setting['lifetime'], 10)
        if COOKIE_SESSIONID in cookie:
            self.session_id=cookie[COOKIE_SESSIONID].value
            self.load()
        else:
            self.data = {}
        self.regenerate_id()
        if random.random() <= GC_PROB:
            self.handler.gc(self.lifetime)
    def load(self):
        data = self.handler.read(self.session_id, self.lifetime)
        try:
            self.data = self.serializer.loads(data)
        except:
            self.data = {}
    def save(self):
        if self.session_id is None:
            self.regenerate_id()
        if self.session_id is not None:
            self.handler.write(self.session_id, self.serializer.dumps(self.data))
#            data = self.handler.read(self.session_id)
#            print(self.data, self.serializer.loads(data.encode('utf-8')))
#            raise Exception(self.serializer.dumps(self.data), self.serializer.loads(data.encode('utf-8')))
    def setvalue(self, key, value):
        self.data[key] = value
    def getvalue(self, key, default=None):
        if key in self.data:
            return self.data[key]
        return default
    def regenerate_id(self):
        for i in range(10):
            session_id = hashlib.md5('%s' % uuid.uuid4()).hexdigest()
            if self.handler.create(session_id):
                break
            else:
                session_id = None
        if session_id is not None:
            self.prev_session_id.append(self.session_id)
            self.session_id = session_id
    def get_session_id(self):
        return self.session_id
    def close(self):
        if self.session_id is not None:
            expires = datetime.datetime.now()+datetime.timedelta(seconds=self.lifetime)
            self.cookie[COOKIE_SESSIONID] = self.session_id
            self.cookie[COOKIE_SESSIONID]["expires"]=expires.strftime("%a, %d-%b-%Y %H:%M:%S JST")
            self.save()
        for prev_id in self.session_id:
            self.handler.delete(prev_id)
        self.handler.close()
