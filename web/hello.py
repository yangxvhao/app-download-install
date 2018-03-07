#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yangxvhao'


def application(envrion, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    print(envrion['PATH_INFO'][1:])
    body = '<h1>hello %s!</h1>' % envrion['PATH_INFO'][1:] or 'web'
    return [body.encode('utf-8')]
