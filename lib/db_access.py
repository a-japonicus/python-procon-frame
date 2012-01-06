#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        DBアクセサ
# Purpose:
#
# Author:      hatahata
#
# Created:     03/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#--------------
import path
import time
from time import gmtime
import sqlite3
import copy

class DBInitError(Exception):
    """
    DBの初期化エラー
    """
    pass

class DBAccess(object):
    """
    DBのアクセスクラス
    sqliteのみ対応
    """
    def __init__(self, setting):
        self._db_init(setting)
    def __del__(self):
        if self.con:
            self.close()
    def _db_init(self, setting):
        """
        DB初期化
        """
        self.con = None
        try:
            self.clear_prepared_list()
            self.setting = setting
            if self.setting['sql'] == 'sqlite':
                #sqliteを使用
                self.setting_sqlite()
            else:
                raise DBInitError(self.setting)
        except:
            pass
            raise DBInitError(self.setting)
    def setting_sqlite(self):
        """
        sqlite初期化
        """
        self.con = sqlite3.connect(self.setting['db_dir']+self.setting['db'])
        self.con.row_factory = sqlite3.Row
        self.con.isolation_level = None
        self.cur = self.con.cursor()
        self.execute_sql('pragma count_changes=1')
    def clear_prepared_list(self):
        """
        プリペアドステートメントの辞書初期化
        """
        self.prepared_list={}
    def set_prepared_list(self, d):
        """
        辞書セット
        返り値は置き換え文字
        """
        s = '%s' % len(self.prepared_list)
        self.prepared_list[s] = d
        return s
    def get_prepared_list(self):
        """
        置き換え文字と値の辞書
        """
        return self.prepared_list

    def select(self, table, fields=['*'], where={}, limit=None, other=''):
        """
        select発行
        """
        sql = ''
        sql = 'SELECT '
        sql += ','.join([f for f in fields])
        sql += ' FROM %s' % table
        self.clear_prepared_list()
        if len(where) > 0:
            sql += ' WHERE '
            sql += ' AND '.join(['%s=:%s'%(k,self.set_prepared_list(v)) for k,v in where.items()])
        if limit != None:
            sql += ' LIMIT %d' % limit
        sql += ' ' + other
        res = self.execute_sql(sql, self.get_prepared_list())

        return res

    def update(self, table, sets={}, where={}, other=''):
        """
        update発行
        返り値は更新数
        """
        sql = 'UPDATE %s' % table
        self.clear_prepared_list()
        if len(sets) > 0:
            sql += ' SET '
            sql += ','.join(['%s=:%s'%(k,self.set_prepared_list(v)) for k,v in sets.items()])
        if len(where) > 0:
            sql += ' WHERE '
            sql += ' AND '.join(['%s=:%s'%(k,self.set_prepared_list(v)) for k,v in where.items()])

        sql += ' ' + other
        res = self.execute_sql(sql, self.get_prepared_list())
        return res[0][0]

    def insert(self, table, values={}, other=''):
        """
        insert発行
        返り値は挿入数
        """
        sql = 'INSERT INTO %s' % table
        self.clear_prepared_list()
        into_list = []
        value_list = []
        for k,v in values.items():
            into_list.append(k)
            value_list.append(self.set_prepared_list(v))
        sql += '(%s)' % ','.join([k for k in into_list])
        sql += ' VALUES(%s)' % ','.join([':%s' % k for k in value_list])

        sql += ' ' + other
        res = self.execute_sql(sql, self.get_prepared_list())
        return res[0][0]

    def delete(self, table, where={}, other=''):
        """
        delete発行
        返り値は削除数
        """
        sql = 'DELETE FROM %s' % table
        self.clear_prepared_list()
        if len(where) > 0:
            sql += ' WHERE '
            sql += ' AND '.join(['%s=:%s'%(k,self.set_prepared_list(v)) for k,v in where.items()])

        sql += ' ' + other
        res = self.execute_sql(sql, self.get_prepared_list())
        return res[0][0]

    def execute_sql(self, sql, data={}):
        """
        sql実行
        """
#        print(sql, data)
        self.cur.execute(sql, data)
        return self.cur.fetchall()
    def commit(self):
        """
        コミット
        """
        self.con.commit()
    def rollback(self):
        """
        ロールバック
        """
        self.con.rollback()
    def close(self):
        """
        DBのクローズ
        """
        self.con.close()

if __name__ == '__main__':
    setting={
        'sql':'sqlite',
        'db':'sample.db'
    }

    dba = DBAccess(setting)
    try:
        dba.execute_sql('CREATE TABLE session_tbl(session_id CHAR(40), data BLOB, update_time INTEGER)')
    except:
        pass
#    try:
    import pickle
    data = {'a':'test', 'b':'test2'}
    print (dba.insert(table='session_tbl', values={'session_id':'0'}))
    print (dba.update(table='session_tbl', sets={'data':pickle.dumps(data)}))
    print(data)
    d = dba.select(table='session_tbl', fields=['data'], where={'session_id':'0'})
    for v in d:
        print (v)
    print (pickle.dumps(data),d[0]['data'])
    print (pickle.loads(d[0]['data'].encode('utf-8')))
    dba.commit()
#    except:
#        print ('Failed')
#        dba.rollback()
