#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
# 管理员登录验证

import  pymongo
from  bson import  ObjectId
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
        rslt = collection.find({"title":name ,"cata" : cata}, {"name":1})
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

        arrKeyWord = keywords.split(",")

        collection.insert({"title":name, "brand":brand, "cata":cata ,"keywords":arrKeyWord ,
                           "desp":desp,"image":images, "context":context})

        self.write({"content":"产品添加成功", "state":1 })



class listProduct(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        arr_product = []
        item= {}
        collection = self.db.project
        rslt = collection.find({}, {"_id":1 ,"title":1 ,"brand":1 , "cata":1})
        for row_item in rslt:
            item["id"] = str(row_item["_id"])
            item["title"] = row_item["title"]
            item["brand"] = row_item["brand"]
            item["cata"] = row_item["cata"]
            arr_product.append(item)

        self.render("admin/productlist.html",admin_user=admin_user ,arrProduct= arr_product)



class editProduct(common.BaseHandle):
    def get(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        get_dict = {
            "brandlist":[],
            "catalist":[]
        }

        # catalist 默认只添加 研华的catalist
        # collection = self.db.category
        # db_result = collection.find({},{"brandname":1 ,"cataItems":1})
        # get_dict["catalist"] = db_result[0]["cataItems"]
        # for item in db_result:
        #     get_dict["brandlist"].append(item["brandname"])


        pid =self.get_argument("pid")
        collection = self.db.project
        rslt = collection.find({"_id":ObjectId(pid) })
        for item in rslt :
            separator = ","
            strKeywords = separator.join(item["keywords"])
            item["keywords"]=strKeywords

            print item["keywords"]
            self.render("admin/productedit.html" ,admin_user=admin_user , info_dict= get_dict ,productInfo =item)

    def post(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        pid = self.get_argument("pid")
        name = self.get_argument("name")
        cata = self.get_argument("cata")
        brand = self.get_argument("brand")
        keywords= self.get_argument("keywords")
        desp= self.get_argument("desp")
        context = self.get_argument("context")
        images = self.get_argument("image")


        arrKeyWord = keywords.split(",")

        collection = self.db.project
        collection.update({"_id":ObjectId(pid)},{"$set" :{"title":name, "brand":brand, "cata":cata ,"keywords":arrKeyWord ,
                           "desp":desp,"image":images, "context":context}})

        self.write({"content":"修改产品成功", "state":1 })
        pass





class deleProduct(common.BaseHandle):
    def post(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        pid =self.get_argument("pid")

        collection = self.db.project
        db_result = collection.remove({"_id":ObjectId(pid)})
        self.write({"content":"删除成功", "state":1})
