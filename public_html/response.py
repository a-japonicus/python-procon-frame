#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Response
# Purpose:     HTTPレスポンスクラス
#
# Author:      hatahata
#
# Created:     31/12/2011
# Copyright:   (c) hatahata 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Cookie import SimpleCookie
from tag import *
from session import Session

class Response(object):
    """
     HTTPのレスポンスを返すクラス
    """
    def __init__(self, cookie=None, charset='utf-8'):
        self.cookie = cookie
        self.charset = charset
        self.response_headers={}
        self.response_data=[]
        self.set_response_header('Content-type', 'text/html;charset=%s' % charset)
    def set_response_header(self, name, value):
        """
        レスポンスヘッダ追加
        """
        self.response_headers[name] = value
    def clear_response_header(self):
        """
        レスポンスヘッダ削除
        """
        self.response_headers={}
    def make_response_header(self):
        """
        レスポンスヘッダ出力
        """
        header = '\n'.join(['%s: %s' % (k, v) for k,v in self.response_headers.items()]) + '\n'
        if self.cookie != None:
            header += self.cookie.output() + '\n'
        return header
    def add_response_data(self, value):
        """
        レスポンスデータ追加
        """
        self.response_data.append(value)
    def clear_response_bata(self):
        """
        レスポンスデータ削除
        """
        self.response_data=[]
    def make_response_data(self):
        """
        レスポンスデータ出力
        """
        response_data = ''.join(['%s\n' % v for v in self.response_data if v != None])
        return response_data
    def make_output(self):
        """
        レスポンスを出力
        """
        output = ''
        # ヘッダー
        output += self.make_response_header() + '\n'
        # ボディ出力
        output += self.make_response_data()
        return output

    def __str__(self):
        return self.make_output().encode(self.charset)


if __name__ == "__main__":
    response = Response()
    response.set_response_header('Content-type', 'text/html;charset=utf-8')
    response.add_response_data(u'<html><head><title>Responseクラス</title></head><body>Responseクラスのテストページ</body></html>')
    print ('%s'.encode('utf-8') % response)
