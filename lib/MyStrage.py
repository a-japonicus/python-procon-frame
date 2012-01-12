#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        MyStrage
# Purpose:     ストレージクラス
#
# Author:      hatahata
#
# Created:     11/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path

class MyStrage(object):
    def __init__(self, data=None):
        self.data = {}
        if data is not None:
            for key,value in data:
                self.data[key] = data[key]
    def setvalue(self, key, value):
        self.data[key] = value
    def getvalue(self, key, default=None):
        if key in self.data:
            return self.data[key]
        return default
    def items(self):
        return self.data.items()

if __name__ == "__main__":
    pass
