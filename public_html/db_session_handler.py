#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        DBSessionHandler
# Purpose:     DBのセッションハンドラ
#
# Author:      hatahata
#
# Created:     03/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
from time import gmtime
import uuid
import copy
from session_handler import SessionHandler
from db_access import DBAccess

class DBSessionHandler(SessionHandler):
    """
    DBセッションハンドラ
    """
    def __init__(self, setting):
        self.sql_setting = copy.deepcopy(setting['sql_setting'])
        self.session_limit = setting['session_limit']
        self.dba = DBAccess(self.sql_setting)
        self.create_tbl()
        super(DBSessionHandler, self).__init__(self.session_limit)
    def create_tbl(self):
        """
        テーブル生成
        """
        try:
            self.dba.execute_sql('CREATE TABLE session_tbl(session_id CHAR(40) UNIQUE, data BLOB, update_time INTEGER)')
            self.dba.commit()
        except:
            pass
    def create(self, session_id):
        """
        セッション生成
        """
        try:
            self.dba.insert('session_tbl', {'session_id':session_id, 'data':'', 'update_time':time.mktime(gmtime())})
            self.dba.commit()
            return True
        except:
            return False
    def read(self, session_id):
        """
        セッション読み込み
        """
        if session_id != None:
            res = self.dba.select('session_tbl', fields={'data'}, where={'session_id':session_id, 'update_time>':time.mktime(gmtime())-self.session_limit})
            if len(res) == 1:
                return res[0]['data']
        return None
    def write(self, session_id, data):
        """
        セッション書き込み
        """
        if session_id != None:
            res = self.dba.update(table='session_tbl', sets={'data':data, 'update_time':time.mktime(gmtime())}, where={'session_id':session_id})
            print (res)
            if res == 0:
                self.dba.insert('session_tbl', {'session_id':session_id, 'data':data, 'update_time':time.mktime(gmtime())})
            self.dba.commit()

    def delete(self, session_id):
        """
        セッション削除
        """
        if session_id != None:
            self.dba.delete('session_tbl', where={'session_id':session_id})
            self.dba.commit()
    def gc(self):
        """
        ガーベジコレクション
        """
        self.dba.execute_sql('DELETE FROM session_tbl WHERE update_time+:session_limit > :now',{'session_limit':self.session_limit, 'now':time.mktime(gmtime())})
        self.dba.commit()

if __name__ == '__main__':
    setting={
        'sql_setting':{
            'sql':'sqlite',
            'db':'session_db',
        },
        'session_limit':1440
    }
    dba = DBAccess(setting['sql_setting'])
    handler = DBSessionHandler(setting)
    id = None
    for i in range(10):
        data = handler.read(id)
        if data == None:
            data = ''
        print (data)
        handler.delete(id)
        if id == None:
            id = handler.generate_session_id()
        data += 'A'
        handler.write(id, data)
        print (dba.execute_sql('select * from session_tbl'))

