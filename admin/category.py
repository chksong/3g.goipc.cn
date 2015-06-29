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
        for item in collection.find({},{"brandname":1 ,"cataItems":1}):
            if "cataItems" in item:
                listCataName = []
                for cataItem in item["cataItems"]:
                    listCataName.append(cataItem["cataName"])

                cates.append({"brand":item["brandname"],"catalist": listCataName})
            else :
                cates.append({"brand":item["brandname"],"catalist":[]})

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

        self.check_xsrf_cookie()

        brandname = self.get_argument("brandname").strip()
        if not brandname or len(brandname) <6 :
            self.write({"content":"品牌字段为空或者太短", "state":-1})
            return

        collection = self.db.category
        db_result = collection.find_one({"brandname":brandname})
        if not db_result:  #
             collection.insert({"brandname":brandname})
        else  :
            self.write({"content":"品牌已经存在", "state":-1})
            return

        logging.info("[AddBrandName] brandname=%s" % brandname )
        self.write({"content":"成功", "state":1})

# 删除品牌
class deleteBrand(common.BaseHandle):
     def get(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname").strip()
        if not brandname or len(brandname) <6 :
            self.write({"content":"品牌字段为空或者太短", "state":-1})
            return

        collection = self.db.category
        db_result = collection.remove({"brandname":brandname})
        self.write({"content":"删除成功", "state":1})


class editBrand(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname").strip()
        if not brandname:
            return

        collection = self.db.category
        db_result = collection.find_one({"brandname":brandname})
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

        brandname = self.get_argument("brandname").strip()
        if not brandname:
            self.write({"content":"修改branditem参数错误", "state":-1})
            return

        keywords=   self.get_argument("keywords").strip()
        desp =      self.get_argument("descp").strip()

        collection = self.db.category
        collection.update({"brandname" : brandname}, {"$set" : {"keywords":keywords, "Description":desp}})

        self.write({"content":"修改branditem成功", "state":1})


class AddCataName(common.BaseHandle):
    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname").strip()
        if not brandname:
            self.write({"content":"添加branditem参数错误", "state":-1})
            return

        cataname =self.get_argument("cataname").strip()
        if not cataname:
            self.write({"content":"添加cataname参数错误", "state":-1})
            return

        collection = self.db.category
        db_reslut  = collection.find({"cataItems.cataName":cataname})
        if db_reslut.count():
            self.write({"content":"添加产品分类已经存在", "state":-1})
            return
        else :
            collection.update({"brandname":brandname}, {"$push":{"cataItems":{"cataName":cataname}}})
            self.write({"content":"添加产品分类成功", "state":1})



class deleteCataName(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        # brandname = self.get_argument("brandname").strip()
        # if not brandname:
        #     self.write({"content":"删除branditem参数错误", "state":-1})
        #     return

        cataname =self.get_argument("cataItem").strip()
        if not cataname:
            self.write({"content":"删除cataname参数错误", "state":-1})
            return

        collection = self.db.category
        collection.update({"cataItems.cataName":cataname}, {"$pull":{"cataItems":{"cataName":cataname}}})
        self.write({"content":"删除产品分类已经成功", "state":-1})


class editCataName(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        brandname = self.get_argument("brandname").strip()
        if not brandname:
            return

        cataname =self.get_argument("cataItem").strip()
        if not cataname:
            return

        item_cata = {
            "brandname":brandname,
            "cataname":cataname,
            "keywords":"",
            "description":""
        }

        collection = self.db.category
        db_reslut  = collection.find({"cataItems.cataName":cataname},{"cataItems":1,"brandname":1})
        for db_item in db_reslut:
           for cata_item  in  db_item["cataItems"]:
               if  cata_item["cataName"] == cataname:
                   item_cata["brandname"] = db_item["brandname"]
                   if "keywords" in cata_item:
                       item_cata["keywords"]=cata_item["keywords"]
                   if  "Description" in cata_item:
                       item_cata["Description"]= cata_item["Description"]


        self.render("admin/category_cata_Item.html",admin_user=admin_user, cataItem=item_cata)


    def post(self):
        admin_user = self.get_admin_user()
        if not admin_user:
            self.redirect("/")
            return

        cataname =self.get_argument("cataItem").strip()
        if not cataname:
            return

        keywords=   self.get_argument("keywords").strip()
        desp =      self.get_argument("descp").strip()

        collection = self.db.category
        collection.update({"cataItems.cataName":cataname},{"$set":{"cataItems.$.keywords":keywords ,
                                                                   "cataItems.$.Description":desp}})

        self.write({"content":"修改cataItems成功", "state":1})


class getCatalistByBrand(common.BaseHandle):
    def get(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        get_dict = {
            "content":[],
            "state":-1
        }

        brandname = self.get_argument("brandname").strip()
        if not brandname or len(brandname) <4  :
            get_dict["content"] = "品牌字段为空或者太短"
            get_dict["state"] = -1
            self.write(get_dict)
            return

        collection = self.db.category
        db_result = collection.find({"brandname":brandname},{"cataItems":1})
        for item in db_result:
            if "cataItems" in item:
                get_dict["state"] = 1 ;
                get_dict["brandlist"]= item["cataItems"]

        self.write(get_dict)
