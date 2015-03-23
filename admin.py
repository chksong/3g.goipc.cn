#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#
# 后台管理的部分
import  tornado
import  tornado.escape
import  common
import  logging


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(repr(self.request))


class AdminIndex(common.BaseHandle):
    def get(self):
        admin_user = tornado.escape.json_encode(self.get_admin_user())
        if  admin_user == "null"  :
            self.redirect("/admin/login")
            return

        self.render("admin.index.html",name=admin_user)


class AdminLogout(common.BaseHandle):
    def get(self):
        self.clear_cookie("adminuser")
    def post(self):
        self.clear_cookie("adminuser")

class AdminLogin(common.BaseHandle):
    def get(self):
        logging.info("AdminLogin。。。")
        self.render("admin.login.html")

    def post(self):
        admin_user = self.get_argument("username")
        admin_pass = self.get_argument("passwd")
        #模拟认证
        if admin_user == "songchengkui" and admin_pass == "123456":
            self.set_secure_cookie("adminuser",tornado.escape.json_encode(admin_user),expires_days=1)
        #self.write({"content":"成功", "state":1})
        self.redirect("/admin")

class AdminRegister(common.BaseHandle):
    def get(self):
        self.render("admin.register.html")

