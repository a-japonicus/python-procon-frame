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
import path
import os
import time
import datetime
from Cookie import SimpleCookie
from tag import *

class BaseResponse(object):
    """
     HTTPのレスポンスを返すクラス
    """
    def __init__(self, cookie=None, charset='utf-8'):
        if cookie is None:
            cookie=SimpleCookie(os.environ.get('HTTP_COOKIE',''))
        self.cookie = cookie
        self.charset = charset
        self.response_headers={}
        self.response_data=[]
        self.set_response_header('Content-type', 'text/html;charset=%s' % charset)
    def get_charset(self):
        return self.charset
    def set_cookie(self, key, value, lifetime=0):
        """
        クッキーをセット
        """
        expires = datetime.datetime.now()+datetime.timedelta(seconds=lifetime)
        self.cookie[key] = value
        self.cookie[key]["expires"]=expires.strftime("%a, %d-%b-%Y %H:%M:%S JST")
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
    def get_header_list(self):
        ret = []
        for k,v in self.response_headers.items():
            ret.append((k, v))

        for cookie_key,value in self.cookie.items():
            cookie_value = '%s=%s' % (cookie_key, self.cookie[cookie_key].value)
            if hasattr(value, '__iter__'):
                cookie_value += ''.join(['; %s=%s' % (k,v) for k,v in value.items() if v != ''])
            ret.append(('Set-Cookie', cookie_value))

        return ret
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
    def make_response_body(self):
        """
        レスポンスデータ出力
        """
        response_data = ''.join(['%s\n' % v for v in self.response_data if v != None])
        return response_data
    def get_body(self):
        return self.make_response_body().encode(self.charset)
    def make_output(self):
        """
        レスポンスを出力
        """
        output = ''
        # ヘッダー
        output += self.make_response_header() + '\n'
        # ボディ出力
        output += self.make_response_body()
        return output

    def __str__(self):
        return self.make_output().encode(self.charset)


if __name__ == "__main__":
    response = Response()
    response.set_response_header('Content-type', 'text/html;charset=utf-8')
    response.add_response_data(u'<html><head><title>Responseクラス</title></head><body>Responseクラスのテストページ</body></html>')
    print ('%s'.encode('utf-8') % response)
    print (response.get_header_list())
