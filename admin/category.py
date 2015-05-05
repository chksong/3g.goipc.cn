#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
# 管理员登录验证



from lib import common
import  logging

class listCategory(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        cates = [
            {
                "brand": "研华工控产品",
                "cata" : ["工控机","主板", "电源"]
            },
            {
                "brand": "华北工控产品",
                "cata" : ["工控机","主板", "电源"]
            },
            {
                "brand": "凌华公共产品",
                "cata" : ["工控机","主板", "电源"]
            },
        ]

        self.render("admin/category.html",admin_user=admin_user, brands=cates )

    def post(self):
        pass

class AddBrandName(common.BaseHandle):
    def get(self):
        pass

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname")
        if not brandname or len(brandname) <10 :
            self.write({"content":"品牌字段为空或者太短", "state":-1})
            return

        logging.info("[AddBrandName] brandname=%s" % brandname )

        self.write({"content":"成功", "state":1})