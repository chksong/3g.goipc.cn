#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
# 关于公司的介绍的一些页面的后台

import  pymongo
from  bson import  ObjectId
from lib import common
import  logging


class AddGoipcAndNews(common.BaseHandle):
    def get(self):
        pass


class ListGoipcAndNews(common.BaseHandle):
    def get(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        collection = self.db.category
        for item in collection.find({},{"brandname":1 ,"cataItems":1}):
            if "cataItems" in item:
                listCataName = []
                for cataItem in item["cataItems"]:
                    listCataName.append(cataItem["cataName"])

                cates.append({"brand":item["brandname"],"catalist": listCataName})
            else :
                cates.append({"brand":item["brandname"],"catalist":[]})

        self.render("admin/category_list.html",admin_user=admin_user, brands=cates )
        pass

class deleGoipcAndNew(common.BaseHandle):
    def get(self, *args, **kwargs):
        pass

class editGoipcAndNew(common.BaseHandle):
    def get(self, *args, **kwargs):
        pass

