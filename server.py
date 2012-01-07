#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        SimpleCGIServer
# Purpose:     CGIHTTPServerを使用した簡易サーバ
#
# Author:      hatahata
#
# Created:     06/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import BaseHTTPServer
import CGIHTTPServer
import os

# TODO:全てのディレクトリでCGIが動く簡易サーバの作成
# 現在はpublic_html内のみ。サブディレクトリを見てくれない・・・
os.chdir('public_html')
CGIHTTPServer.CGIHTTPRequestHandler.cgi_directories = ['/']
BaseHTTPServer.HTTPServer(('', 80), CGIHTTPServer.CGIHTTPRequestHandler).serve_forever()
