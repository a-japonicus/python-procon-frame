#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Tag
# Purpose:     HTMLタグ
#              valueに追加することで入れ子にすることが可能
#
# Author:      hatahata
#
# Created:     31/12/2011
# Copyright:   (c) hatahata 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# インデント
INDENT = '  '

class Tag(object):
    """
    HTMLタグクラス
    """
    def __init__(self, tag='', values=None, elements={}):
        self.tag = tag
        self.values = []
        if values:
            self.add_value(values)
        self.elements = elements.copy()
    def set_tag(self, tag):
        self.tag = tag
    def add_value(self, values):
        if hasattr(values, '__iter__'):
            for v in values:
                self.values.append(v)
        else:
            self.values.append(values)
    def set_element(self, key, value):
        self.elements[key] = value
    def set_tag(self, tag):
        self.tag = tag
    def make_output(self, indent=''):
        """
        タグを生成
        """
        output = indent
        # タグを作成
        output += '<' + self.tag
        output += ''.join([' %s="%s"' % (k,v) for k,v in self.elements.items()])

        value_size = len(self.values)
        if value_size == 1  and  (isinstance(self.values[0], unicode) or isinstance(self.values[0], str)):
            # valueが一つで文字列であれば1行で表示
            output += u'>%s</%s>' % (self.values[0], self.tag)
        elif value_size > 0:
            # valueが複数もしくは文字列以外なら1行1value表示
            output += '>\n'
            tag_tab = indent + INDENT
            for v in self.values:
                if (v == None):
                    continue
                if isinstance(v, Tag):
                    out_str = v.make_output(tag_tab)
                else:
                    out_str = tag_tab + v
                output += '%s\n' % out_str
            output += '%s</%s>' % (indent, self.tag)
        else:
            # valueがなければ閉じる
            output += '/>'
        return output
    def __str__(self):
        return self.make_output()

class DummyTag(Tag):
    """
    ダミータグ
    出力されない
    """
    def __init__(self):
        super(DummyTag, self).__init__()
    def make_output(self, tab=''):
        return ''
    def __str__(self):
        return ''

class HtmlTag(Tag):
    """
    htmlタグ
    """
    def __init__(self, values=None, elements={}):
        super(HtmlTag, self).__init__('html', values, elements)

class HeadTag(Tag):
    """
    headタグ
    """
    def __init__(self, values=None, elements={}):
        super(HeadTag, self).__init__('head', values, elements)

class BodyTag(Tag):
    """
    bodyタグ
    """
    def __init__(self, values=None, elements={}):
        super(BodyTag, self).__init__('body', values, elements)

class MetaTag(Tag):
    """
    metaタグ
    """
    def __init__(self, elements={}):
        super(MetaTag, self).__init__('meta', None, elements)

class RedirectTag(MetaTag):
    """
    リダイレクトタグ
    """
    def __init__(self, url, time=0, elements={}):
        super(RedirectTag, self).__init__(elements)
        self.set_element('http-equiv', 'refresh')
        self.set_element('content', '%d;url=%s' % (time, url))

class DivTag(Tag):
    """
    divタグ
    """
    def __init__(self, id='', values=None, elements={}):
        super(DivTag, self).__init__('div', values, elements)
        self.set_element('id', id)

class ATag(Tag):
    """
    aタグ
    """
    def __init__(self, href='', values=None, elements={}):
        if values == None:
            values = href
        super(ATag, self).__init__('a', values, elements)
        self.set_element('href', href)

class TitleTag(Tag):
    """
    titleタグ
    """
    def __init__(self, values=None, elements={}):
        super(TitleTag, self).__init__('title', values, elements)

class FormTag(Tag):
    """
    formタグ
    """
    def __init__(self, action, method='POST', values='', elements={}):
        super(FormTag, self).__init__('form', values, elements)
        self.set_element('action', action)
        self.set_element('method', method)

class InputTag(Tag):
    """
    inputタグ
    """
    def __init__(self, name=None, value=None, elements={}):
        super(InputTag, self).__init__('input', None, elements)
        if name != None:
            self.set_element('name', name)
        if value != None:
            self.set_element('value', value)

class HiddenTag(InputTag):
    """
    hiddenタグ
    """
    def __init__(self, name=None, value=None, elements={}):
        super(HiddenTag, self).__init__(name, value, elements)
        self.set_element('type', 'hidden')

class PasswordTag(InputTag):
    """
    passwordタグ
    """
    def __init__(self, name=None, value=None, elements={}):
        super(PasswordTag, self).__init__(name, value, elements)
        self.set_element('type', 'password')

class SubmitTag(InputTag):
    """
    submitタグ
    """
    def __init__(self, name=None, value=None, elements={}):
        super(SubmitTag, self).__init__(name, value, elements)
        self.set_element('type', 'submit')

class TextTag(InputTag):
    """
    textタグ
    """
    def __init__(self, name=None, value=None, elements={}):
        super(TextTag, self).__init__(name, value, elements)
        self.set_element('type', 'text')

class PTag(Tag):
    """
    pタグ
    """
    def __init__(self, values=None, elements={}):
        super(PTag, self).__init__('p', values, elements)

class H1Tag(Tag):
    """
    h1のタグ
    """
    def __init__(self, values=None, elements={}):
        super(H1Tag, self).__init__('h1', values, elements)

class H2Tag(Tag):
    """
    h2のタグ
    """
    def __init__(self, values=None, elements={}):
        super(H2Tag, self).__init__('h2', values, elements)

class H3Tag(Tag):
    """
    h3のタグ
    """
    def __init__(self, values=None, elements={}):
        super(H3Tag, self).__init__('h3', values, elements)

class H4Tag(Tag):
    """
    h4のタグ
    """
    def __init__(self, values=None, elements={}):
        super(H4Tag, self).__init__('h4', values, elements)

class H5Tag(Tag):
    """
    h5のタグ
    """
    def __init__(self, values=None, elements={}):
        super(H5Tag, self).__init__('h5', values, elements)

class H6Tag(Tag):
    """
    h6のタグ
    """
    def __init__(self, values=None, elements={}):
        super(H6Tag, self).__init__('h6', values, elements)

class HRTag(Tag):
    """
    hrのタグ
    """
    def __init__(self, values=None, elements={}):
        super(HRTag, self).__init__('hr', values, elements)
