#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
# 管理员登录验证

import  pymongo
from lib import common
import  logging


class testUeditor(common.BaseHandle):
    def get(self):

        self.render("admin/ueditor.html")

    def post(self):
        pass



class addProduct(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        get_dict = {
            "brandlist":[],
            "catalist":[]
        }

        # catalist 默认只添加 研华的catalist
        collection = self.db.category
        db_result = collection.find({},{"brandname":1 ,"cataItems":1})
        get_dict["catalist"] = db_result[0]["cataItems"]
        for item in db_result:
            get_dict["brandlist"].append(item["brandname"])

        print get_dict


        self.render("admin/productadd.html",admin_user=admin_user,info_dict=get_dict)

    def post(self):
        pass