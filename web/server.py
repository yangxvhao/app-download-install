#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yangxvhao'


from wsgiref.simple_server import make_server
from web.hello import application

http = make_server('', 8081, application)
http.serve_forever()
