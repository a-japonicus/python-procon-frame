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
import CGIHTTPServer

# TODO:全てのディレクトリでCGIが動く簡易サーバの作成
# 現在はpublic_html内のみ。サブディレクトリを見てくれない・・・
CGIHTTPServer.CGIHTTPRequestHandler.cgi_directories = ['/public_html']
CGIHTTPServer.test()
