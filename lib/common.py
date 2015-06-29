#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#
#

import  logging

import tornado
import tornado.web

from  bson.objectid  import  ObjectId
from  crypto import  get_random_string

from  models import  AdminMixin
import datetime

from lib.crypto import PasswordCrypto

class BaseHandle(tornado.web.RequestHandler, AdminMixin):
    @property
    def db(self):
        return  self.application.db

    def get_current_user(self):
        pass

    def get_admin_user(self):
        token_id = self.get_secure_cookie("token_id")
        if not  token_id:
            return None
        token = token_id.split("/")[0]
        admin_id =   token_id.split("/")[1]

        db_admin = self.get_admin_by_id( ObjectId(admin_id) )
        if db_admin == None :
            return None

        if db_admin["token"] != token.strip():
            return None

        now_diff = datetime.datetime.utcnow() - db_admin["token_time"]
        #证书超时
        if now_diff > datetime.timedelta(hours =5 ):
            print "证书超时。"
            rand_string = get_random_string()
            self.update_admin_salt(admin_id ,rand_string)
            self.update_admin_token_time(admin_id)
            self.clear_cookie("token")
            self.redirect("/")
        else :
            return db_admin["name"]

    def error404(self, reason):
        self.render("mobile/e404_why.html",why=reason)

