#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        user
# Purpose:     ユーザ関係
#
# Author:      hatahata
#
# Created:     08/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import uuid
import hashlib
from lib import DBAccess

class User(object):
    """
    ユーザ用ライブラリ
    """
    def __init__(self, username, password=None, salt=''):
        self.dba = DBAccess.order()
        self.data = {}
        self.select(username, password, salt)
    def exist(self):
        return self.getvalue('username') is not None
    def setvalue(self, key, value):
        self.data[key] = value
    def getvalue(self, key, default=None):
        if key in self.data:
            return self.data[key]
        return default
    def select(self, username, password=None, salt=''):
        self.data = {}
        if username is None or not username.isalnum():
            return False
        where = {'username':username}
        if password is not None:
            if not password.isalnum():
                return False
            where['password'] = self.password_hash(username, password, salt)
        data = self.dba.select('user_tbl', '*', where)
        if len(data) != 1:
            return False
        self.data = data[0]
        return True
    def update(self):
        if self.exist():
            if self.dba.update('user_tbl', self.data, {'username':self.data['username']}) == 1:
                self.dba.commit()
                return True
            self.dba.rollback()
        return False
    def insert(self):
        if self.exist():
            try:
                self.dba.insert('user_tbl', self.data)
                self.dba.commit()
                return True
            except:
                self.dba.rollback()
        return False
    def delete(self):
        if self.exist():
            if self.dba.delete('user_tbl', {'username':self.data['username']}) == 1:
                self.dba.commit()
                return True
            self.dba.rollback()
        return False
    def reset_hash(self):
        if self.exist():
            for i in range(10):
                hash = hashlib.md5(str(uuid.uuid4())).hexdigest()
                if len(self.dba.select('user_tbl', 'hash', {'hash':hash})) == 0:
                    self.dba.update('user_tbl', {'hash':hash}, {'username':self.data['username']})
                    self.data['hash'] = hash
                    return True
        return False
    def reset_password(self, old_password=None, new_password=None, salt='', force=False):
        if not self.exist():
            return False
        if not force:
            if old_password is None or not old_password.isalnum():
                return False
            old_pass_hash = self.password_hash(self.data['username'], old_password, salt)
            if self.data['password'] != old_pass_hash:
                return False

        if new_password is None or not new_password.isalnum():
            return False
        new_pass_hash = self.password_hash(self.data['username'], new_password, salt)
#        if self.dba.update('user_tbl',{'password':new_pass_hash}, {'username':self.data['username']}) != 1:
#            return False
        self.data['password'] = new_pass_hash
        return True
    def password_hash(self, username, password, salt=''):
        return hashlib.sha256(salt + '' + username + ':' + password).hexdigest()
        
        