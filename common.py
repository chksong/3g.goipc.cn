#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#
# 后台管理的部门

import  logging

import tornado
import tornado.web



class BaseHandle(tornado.web.RequestHandler):
    @property
    def db(self):
        return  self.application.db

    def get_current_user(self):
        return  self.get_secure_cookie("user")

    def get_admin_user(self):
        return  self.get_secure_cookie("adminuser")

    def on_connection_close(self):
        logging.debug("[on_connection_close]")
        self.clear_all_cookies();