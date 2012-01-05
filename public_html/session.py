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
import copy
from Cookie import SimpleCookie

class Session(object):
    """
    セッション管理クラス
    """
    def __init__(self, cookie, handler, setting):
        self.cookie = cookie
        self.setting = copy.deepcopy(setting)
        self.handler = handler
        self.serializer = pickle
        self.session_id = None
        if 'SESSIONID' in cookie:
            self.session_id=cookie['SESSIONID'].value
            self.load()
        else:
            self.session_id = self.generate_id()
            self.data = {}
    def load(self):
        data = self.handler.read(self.session_id)
        try:
            self.data = self.serializer.loads(data.encode('utf-8'))
        except:
            self.data = {}
    def save(self):
        if self.session_id == None:
            self.session_id = self.generate_id()
        if self.session_id != None:
             self.handler.write(self.session_id, self.serializer.dumps(self.data))
#             data = self.handler.read(self.session_id)
#             raise Exception(self.serializer.dumps(self.data), self.serializer.loads(data.encode('utf-8')))
    def setvalue(self, key, value):
        self.data[key] = value
    def getvalue(self, key, default=None):
        if key in self.data:
            return self.data[key]
        return default
    def regenerate_id(self):
        for i in range(10):
            session_id = '%s' % uuid.uuid4()
            if self.handler.create(session_id):
                break
            else:
                session_id = None
        return session_id
    def get_session_id(self):
        return self.session_id
