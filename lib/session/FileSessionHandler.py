#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        ファイルセッションハンドラ
# Purpose:     ファイルのセッションハンドラ
#
# Author:      hatahata
#
# Created:     08/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
import os
import datetime
import time
from SessionHandler import SessionHandler

class FileSessionHandler(SessionHandler):
    """
    セッションハンドラ基本クラス
    """
    def __init__(self, setting):
        self.setting = setting
        self.path = os.path.join(os.getcwd(), self.setting['path'])
    def create(self, session_id):
        """
        セッション生成
        """
        result = False
        session_file = self._session_file(session_id)
        try:
            lock_dir = session_file+'.lock'
            os.mkdir(lock_dir)
            if not os.path.exists(session_file):
                try:
                    with open(session_file, 'w') as f:
                        result = True
                except:
                    pass
            os.rmdir(lock_dir)
        except:
            pass
        return result
    def read(self, session_id, lifetime):
        """
        セッション読み込み
        """
        data = None
        session_file = self._session_file(session_id)
        try:
            m = os.stat(session_file)
            file_lifetime = time.mktime(datetime.datetime.now().timetuple()) - lifetime
            if m.st_mtime > file_lifetime:
                f = open(session_file, 'rb')
                data = f.read()
        except:
            data = None
        return data
    def write(self, session_id, data):
        """
        セッション書き込み
        """
        session_file = self._session_file(session_id)
        try:
            with open(session_file, 'wb') as f:
                data = f.write(data)
        except:
            pass
    def delete(self, session_id):
        """
        セッション削除
        """
        session_file = self._session_file(session_id)
        try:
            os.remove(session_file)
        except:
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
    def _session_file(self, session_id):
        return os.path.join(self.path, '%s'%session_id)
    def gc(self, lifetime):
        """
        ガーベジコレクション
        """
        file_lifetime = time.mktime(datetime.datetime.now().timetuple()) - lifetime
        for filename in os.listdir(self.path):
            try:
                filepath = self._session_file(filename)
                m = os.stat(filepath)
                if m.st_mtime > file_lifetime:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                    else:
                        # ロックファイルもlifetimeで削除
                        os.rmdir(filepath)
            except:
                pass




if __name__ == '__main__':
    pass
