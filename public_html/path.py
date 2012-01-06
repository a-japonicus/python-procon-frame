#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        path
# Purpose:     パスの設定
#
# Author:      hatahata
#
# Created:     07/01/2012
# Copyright:   (c) hatahata 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import os

# rootディレクトリ(public_htmlの親ディレクトリ)
ROOT_DIR = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(ROOT_DIR)
# libディレクトリのパス
sys.path.append(os.path.join(ROOT_DIR, './lib'))
# sesisonディレクトリのパス
sys.path.append(os.path.join(ROOT_DIR, './lib/session'))
# pageディレクトリのパス
sys.path.append(os.path.join(ROOT_DIR, './page'))