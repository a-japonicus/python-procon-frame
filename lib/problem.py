#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Problem
# Purpose:     問題
#
# Author:      hatahata
#
# Created:     14/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path
from lib import DBAccess
from lib.user import User

class Problem(object):
    """
    問題クラス
    """
    def __init__(self, problem_id=None):
        self.dba = DBAccess.order()
        self.data = {}
        if problem_id != None:
            self.select(problem_id)
    def getvalue(self, key, default=None):
        if key in self.data:
            return self.data[key]
        return default
    def setvalue(self, key, value):
        self.data[key] = value
    def __setitem__(self, key, value):
        return self.setvalue(key, value)
    def __getitem__(self, key):
        return self.getvalue(key)
    def correct(self):
        """
        整合性チェック
        """
        if self.getvalue('title') is None or self.getvalue('data') is None or self.getvalue('user_id') is None:
            return False
        return True
    def select(self, problem_id):
        self.data = {}
        ret = self.dba.select('problem_tbl', '*', {'id':problem_id})
        if len(ret) != 1:
            return False
        self.data = ret[0]
        return True
    def insert(self):
        ret = self.dba.insert('problem_tbl', self.data)
        if ret == 1:
            return True
        return False
    def items(self):
        return self.data.items()

def get_problems():
    problems = []
    dba = DBAccess.order()
    res = dba.select('problem_tbl', '*')
    for data in res:
        p = Problem()
        for k,v in data.items():
            p.setvalue(k,v)
        problems.append(p)
    return problems

if __name__ == '__main__':
    pass
