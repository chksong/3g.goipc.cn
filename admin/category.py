#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
# 管理员登录验证



from lib import common




class listCategory(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        self.render("admin/category.html",admin_user=admin_user)

    def post(self):
        pass

class BandAdd(common.BaseHandle):
    def get(self):
        pass

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")