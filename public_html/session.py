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
        Exception(self.setting)
        self.lifetime = int(self.setting['lifetime'], 10)
        if 'SESSIONID' in cookie:
            self.session_id=cookie['SESSIONID'].value
            self.load()
        else:
            self.session_id = self.regenerate_id()
            self.data = {}
        if random.random() <= GC_PROB:
            self.handler.gc(self.lifetime)
    def load(self):
        data = self.handler.read(self.session_id, self.lifetime)
        print(data)
        try:
            self.data = self.serializer.loads(data.encode('utf-8'))
        except:
            self.data = {}
    def save(self):
        if self.session_id == None:
            self.session_id = self.regenerate_id()
        if self.session_id != None:
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
        return session_id
    def get_session_id(self):
        return self.session_id
    def close(self):
        expires = datetime.datetime.now()+datetime.timedelta(seconds=self.lifetime)
        self.cookie['SESSIONID'] = self.session_id
        self.cookie['SESSIONID']["expires"]=expires.strftime("%a, %d-%b-%Y %H:%M:%S JST")
        self.save()
        self.handler.close()
