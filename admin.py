#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#
# 后台管理的部分
import  tornado
import  common

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(repr(self.request))


class AdminIndex(common.BaseHandle):
    def get(self):
         self.render("admin.index.html",lorm="xxxxx")
