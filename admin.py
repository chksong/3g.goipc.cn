#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#
# 后台管理的部分
import  tornado
import  tornado.escape
import  common

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(repr(self.request))


class AdminIndex(common.BaseHandle):
    def get(self):
        if not self.get_current_user():
            self.redirect("/admin/login")
            return

        name = tornado.escape.xhtml_escape(self.get_current_user())
        self.render("admin.index.html",name=name)


class AdminLogin(common.BaseHandle):
    def get(self):
        self.render("admin.login.html")


class AdminRegister(common.BaseHandle):
    def get(self):
        self.render("admin.register.html")

class AdminCheckValid(common.BaseHandle):
    def post(self):
        admin_user = self.get_argument("username")
        admin_pass = self.get_argument("passwd")

        self.set_secure_cookie("adminuser",tornado.escape.json_encode(admin_user))
        self.write({"content":"成功", "state":1})
