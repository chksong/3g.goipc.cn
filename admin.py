#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#
# 后台管理的部分
from  tornado.log import  access_log
import  logging
import  re

import  tornado
import  tornado.escape

from lib import common
from lib.crypto import PasswordCrypto
from lib.crypto import get_random_string


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(repr(self.request))


class AdminIndex(common.BaseHandle):
    def get(self):
        admin_user = tornado.escape.json_encode(self.get_admin_user())
        if  admin_user == "null"  :
            self.redirect("/admin/login")
            return

        self.render("admin/index.html",name=admin_user)


class AdminLogout(common.BaseHandle):
    def get(self):
        self.clear_cookie("adminuser")
    def post(self):
        self.clear_cookie("adminuser")

class AdminLogin(common.BaseHandle):
    def get(self):
        logging.info("AdminLogin。。。")
        self.render("admin/login.html",message="")

    def post(self):
        admin_user_email = self.get_argument("username")
        admin_pass = self.get_argument("passwd")

        if (not admin_user_email) or (not admin_pass):
            self.redirect("/admin/login")
            return

        pattern = r'^.+@goipc.cn$'
        if isinstance(pattern ,basestring):
            pattern = re.compile(pattern,flags=0)

        if not pattern.match(admin_user_email):
            self.render("admin/login.html", message="用户名格式不正确")
            return

        result_user = self.get_admin_by_email(admin_user_email)
        if not result_user:
            access_log.error("Login Error for email %s" % admin_user_email)
            self.render("admin/login.html", message="不存在的用户名")
            return

        encryped_pass = result_user["passwd"]
        if PasswordCrypto.authenticate(admin_pass,encryped_pass):
            token = get_random_string()
            self.update_admin_salt(result_user["_id"],token)
            self.update_admin_token_time(result_user["_id"])

            token_id = token + "/"  + str(result_user["_id"])
            self.set_secure_cookie("token_id",str(token_id))
        else:
            access_log.error("login Error for passwd %s!" % admin_pass)
            self.render("admin/login.html", message="密码错误")
            return

        self.redirect("/admin")


        #模拟认证
        #if admin_user == "songchengkui" and admin_pass == "123456":
        #   self.set_secure_cookie("adminuser",tornado.escape.json_encode(admin_user),expires_days=1)
        #self.write({"content":"成功", "state":1})


class AdminRegister(common.BaseHandle):
    def get(self):
        self.render("admin.register.html")

