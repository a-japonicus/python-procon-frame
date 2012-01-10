#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Request
# Purpose:     HTTPリクエストクラス
#
# Author:      hatahata
#
# Created:     11/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import path

class Request(object):
    """
     HTTPのリクエストを持つクラス
    """
    def __init__(self):
        self.data = {}
    def set(self, key, value):
        self.data[key] = value
    def get(self, key):
        return self.data[key]

if __name__ == "__main__":
    pass