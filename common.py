#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#
# 后台管理的部门

import tornado



class BaseHandle(tornado.web.RequestHandler):
    @property
    def db(self):
        return  self.application.db