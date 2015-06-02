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

        #print get_dict
        #get_dict["productname"]="IPC610"



        self.render("admin/productadd.html",admin_user=admin_user,info_dict=get_dict)

    def post(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        name = self.get_argument("name")
        cata = self.get_argument("cata")
        brand = self.get_argument("brand")
        collection = self.db.project

        rslt = collection.find({"name":name ,"cata" : cata}, {"name":1})
        if rslt.count():
            get_dict = {
                "content":"产品名称已经存在",
                "state":-1 ,
            }
            self.write(get_dict)


        brand = self.get_argument("brand")
        keywords= self.get_argument("keywords")
        desp= self.get_argument("desp")
        context = self.get_argument("context")
        images = self.get_argument("image")

        collection.insert({"name":name, "brand":brand, "cata":cata ,"keywords":keywords ,
                           "desp":desp,"image":images, "context":context})

        self.write({"content":"产品添加成功", "state":1 ,})

class listProduct(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        self.render("admin/productadd.html",admin_user=admin_user,info_dict=get_dict)


