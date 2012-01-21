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
import copy

class DBInitError(Exception):
    """
    DBの初期化エラー
    """
    pass

# シングルトン
_dba = None
def create(setting):
    """
    DBAccessのインスタンス作成
    """
    global _dba
    if _dba == None:
        _dba = DBAccess(setting)
    return _dba
def order():
    """
    DBAccessのシングルトン
    """
    global _dba
    if _dba is None:
        raise DBInitError(u'DBAccess未初期化')
    return _dba

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DBAccess(object):
    """
    DBのアクセスクラス
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
        self.clear_prepared_list()
        self.setting = setting
        if self.setting['sql'] == 'sqlite':
            #sqliteを使用
            self.setting_sqlite()
        elif self.setting['sql'] == 'mysql':
            #mysqlを使用
            self.setting_mysql()
        else:
            raise DBInitError(self.setting)
    def setting_mysql(self):
        """
        mysql(pymysql)初期化
        """
        import pymysql
        from pymysql.cursors import DictCursor
        self.con = pymysql.connect(host=self.setting['host'], port=int(self.setting['port']), user=self.setting['user'], passwd=self.setting['passwd'], db=self.setting['db'])
        self.cur = self.con.cursor(DictCursor)
        self.prepared_char = '%s'
    def setting_sqlite(self):
        """
        sqlite初期化
        """
        import sqlite3
        database = self.setting['host']+self.setting['db']
        self.con = sqlite3.connect(database)
        self.con.row_factory = dict_factory
        self.con.isolation_level = None
        self.cur = self.con.cursor()
        self.execute_sql('pragma count_changes=1')
        self.prepared_char = '?'
    def clear_prepared_list(self):
        """
        プリペアドステートメントの辞書初期化
        """
#        self.prepared_list={}
        self.prepared_list=[]
    def set_prepared_list(self, d):
        """
        辞書セット
        返り値は置き換え文字
        """
#        s = '%d' % len(self.prepared_list)
#        self.prepared_list[s] = d
#        return s
        self.prepared_list.append(d)
        return self.prepared_char
    def get_prepared_list(self):
        """
        置き換え文字と値の辞書
        """
        return self.prepared_list

    def _create_where(self, where):
        """
        where文作成
        """
        sql_where = ''
        if len(where) > 0:
            sql_where += ' WHERE'
            items = where.items()
            for i in range(len(items)):
                if i > 0:
                    sql_where += ' AND'
                # whereの最後が比較演算子であれば=を付加しない
                if items[i][0][-1] in ('=', '<', '>'):
                    sql_where += ' %s%s'%(items[i][0], self.set_prepared_list(items[i][1]))
                else:
                    sql_where += ' %s=%s'%(items[i][0], self.set_prepared_list(items[i][1]))
        return sql_where
    def select(self, table, fields='*', where={}, order=[], limit=None):
        """
        select発行
        """
        sql = ''
        sql = 'SELECT '
        if hasattr(fields, '__iter__'):
            sql += ','.join([f for f in fields])
        else:
            sql += fields
        sql += ' FROM %s' % table
        self.clear_prepared_list()
        sql += self._create_where(where)
        if len(order) > 0:
            sql += ' ORDER BY '
            sql += ','.join(['%s'%v for v in order])
        if limit != None:
            sql += ' LIMIT %d' % limit

        res = self.execute_sql(sql, self.get_prepared_list())

        return res

    def update(self, table, sets={}, where={}):
        """
        update発行
        返り値は更新数
        """
        sql = 'UPDATE %s' % table
        self.clear_prepared_list()
        if len(sets) > 0:
            sql += ' SET '
            sql += ','.join(['%s=%s'%(k,self.set_prepared_list(v)) for k,v in sets.items()])
        sql += self._create_where(where)

        res = self.execute_sql(sql, self.get_prepared_list())
        return self.cur.rowcount

    def insert(self, table, values={}):
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
        sql += ' VALUES(%s)' % ','.join(['%s' % k for k in value_list])

        res = self.execute_sql(sql, self.get_prepared_list())
        return self.cur.rowcount

    def delete(self, table, where={}):
        """
        delete発行
        返り値は削除数
        """
        sql = 'DELETE FROM %s' % table
        self.clear_prepared_list()
        if len(where) > 0:
            sql += ' WHERE '
            sql += ' AND '.join(['%s=%s'%(k,self.set_prepared_list(v)) for k,v in where.items()])

        res = self.execute_sql(sql, self.get_prepared_list())
        return self.cur.rowcount

    def execute_sql(self, sql, data=[]):
        """
        sql実行
        """
        # プレースホルダの置き換え
        if self.setting['sql'] == 'sqlite':
            sql = sql.replace('%s','?')
            try:
                ret = self.cur.execute(sql, data)
                return self.cur.fetchall()
            except:
                import sys
                print ('SQL ERROR', sys.exc_info())
            return []
        if self.setting['sql'] == 'mysql':
            sql = sql.replace('?','%s')
            # 文字コードをutf-8にエンコード
            encoded_data = []
            for v in data:
                if isinstance(v, unicode):
                    v = v.encode('utf-8')
                encoded_data.append(v)
            try:
                ret = self.cur.execute(sql.encode('utf-8'), encoded_data)
            except:
                import sys
                print ('SQL ERROR', sys.exc_info())
            rows = self.cur.fetchall()
            if rows:
                # 文字コードをunicodeにエンコード
                ret_rows = []
                for row in rows:
                    r = {}
                    for k,v in row.items():
                        if isinstance(v, str):
                            v = unicode(v, 'utf-8')
                        r[k] = v
                    ret_rows.append(r)
                return ret_rows

            return []

#        return self.cur.fetchall()
    def rowcount(self):
        """
        行の数
        """
        return self.cur.rowcount
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
        self.cur.close()
        self.con.close()

if __name__ == '__main__':
    setting_mysql={
        'sql':'mysql',
        'host':'localhost',
        'db':'sampledb',
        'port':3306,
        'user':'root',
        'passwd':'admin',
    }
    setting_sqlite={
        'sql':'sqlite',
        'host':'',
        'db':':memory:',
    }

    dba = DBAccess(setting_mysql)
#    dba = DBAccess(setting_sqlite)
    try:
        dba.execute_sql('CREATE TABLE session_tbl(session_id CHAR(40), data BLOB, update_time INTEGER)')
    except:
        pass
#    try:
    import pickle
    data = {'a':'test', 'b':'test2'}
    print (dba.insert(table='session_tbl', values={'session_id':'0'}))
    print (dba.insert(table='session_tbl', values={'session_id':'1'}))
    print (dba.insert(table='session_tbl', values={'session_id':'2'}))
    print (dba.update(table='session_tbl', sets={'data':pickle.dumps(data)}))
    d = dba.select(table='session_tbl', fields='*', where={'session_id>':'0','data>':'2'}, order=['session_id desc'])
    for v in d:
        print (v)
    print (dba.delete(table='session_tbl'))
    print(data)
    dba.commit()
    dba.close()
#    except:
#        print ('Failed')
#        dba.rollback()
