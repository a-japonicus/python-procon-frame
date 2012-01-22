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

if __name__ == "__main__":
    import sys
    sys.path.append('public_html')
    import BaseHTTPServer
    import CGIHTTPServer
    import os
    from wsgiref import simple_server
    from wsgi import application
    os.chdir('public_html')
    server = simple_server.make_server("", 80, application)
    print ('Server recv start')
    server.serve_forever()
