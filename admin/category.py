#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
# 管理员登录验证


import  pymongo
from lib import common
import  logging

class listCategory(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        cates= []
        collection = self.db.category
        for item in collection.find({},{"bandname":1}):
            cates.append({"brand":item["bandname"],"cata":[]})
            pass


        # cates = [
        #     {
        #         "brand": "凌华公共产品",
        #         "cata" : ["工控机","主板", "电源"]
        #     },
        # ]

        self.render("admin/category_list.html",admin_user=admin_user, brands=cates )

    def post(self):
        pass

# 快捷的添加 品牌
class AddBrandName(common.BaseHandle):
    def get(self):
        pass

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname")
        if not brandname or len(brandname) <6 :
            self.write({"content":"品牌字段为空或者太短", "state":-1})
            return

        collection = self.db.category
        db_result = collection.find_one({"bandname":brandname})
        if not db_result:  #
             collection.insert({"bandname":brandname})
        else  :
           pass

        logging.info("[AddBrandName] brandname=%s" % brandname )
        self.write({"content":"成功", "state":1})

# 删除品牌
class deleteBrand(common.BaseHandle):
     def get(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname")
        if not brandname or len(brandname) <6 :
            self.write({"content":"品牌字段为空或者太短", "state":-1})
            return

        collection = self.db.category
        db_result = collection.remove({"bandname":brandname})
        self.write({"content":"删除成功", "state":1})


class editBrand(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname")
        if not brandname:
            return

        collection = self.db.category
        db_result = collection.find_one({"bandname":brandname})
        brand_items= {}
        brand_items["brandname"] = brandname

        if "keywords" in db_result:
            brand_items["keywords"] = db_result["keywords"]
        else:
            brand_items["keywords"] = ""

        if "Description" in db_result:
            brand_items["Description"] = db_result["Description"]
        else:
            brand_items["Description"] = ""


        self.render("admin/category_item.html",admin_user=admin_user, brandItems=brand_items)

    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname")
        if not brandname:
            self.write({"content":"修改branditem参数错误", "state":-1})
            return

        keywords=   self.get_argument("keywords")
        desp =      self.get_argument("descp")

        collection = self.db.category
        collection.update({"bandname" : brandname}, {"$set" : {"keywords":keywords, "Description":desp}})

        self.write({"content":"修改branditem成功", "state":1})


class AddCataName(common.BaseHandle):
    def post(self):
        pass

class editCataName(common.BaseHandle):
    def post(self):
        pass
    def get(self):
        pass

class deleteCataName(common.BaseHandle)
    def post(self):
        pass
