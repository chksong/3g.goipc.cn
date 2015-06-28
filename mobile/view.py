#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
#  产看文章内容
#  2015-6-21 日


from  tornado.log import  access_log
import  logging
import  re

import  tornado
import  tornado.escape


from lib import common

class viewUS(common.BaseHandle):
    def get(self, *args, **kwargs):
        if len(args) != 1 :
             self.render("e404_why.html",why="输入参数错误")

        info_dict = {}

        title = args[0]
        collection = self.db.NEWS
        rslt = collection.find({"title":title })
        for item in rslt :
            separator = ","
            strKeywords = separator.join(item["keywords"])
            item["keywords"]=strKeywords

            info_dict["keywords"] = strKeywords
            info_dict["desp"] = item["desp"]

            self.render("mobile/news.html",newsItem =item, infodict=info_dict)


class ViewProduct(common.BaseHandle):
    def get(self, *args, **kwargs):
        if len(args) != 2:
            self.render("e404_why.html",why="输入参数错误")

        cata = args[0]
        title = args[1]
        info_dict = {}

        collection = self.db.project
        collection.update({"title":title ,"cata" : cata},{"$inc":{"readtimes":1}})

        rslt = collection.find({"title":title ,"cata" : cata})
        for item in rslt:
            separator = ","
            strKeywords = separator.join(item["keywords"])
            item["keywords"]=strKeywords

            info_dict["keywords"] = strKeywords
            info_dict["desp"] = item["desp"]

            self.render("mobile/product.html",newsItem =item, infodict=info_dict)
            return

        if 0 == rslt.count():
            self.render("e404_why.html",why="产品不存在")

class ListCata(common.BaseHandle):
    def get(self, *args, **kwargs):
        if len(args) != 1:
            self.render("e404_why.html",why="输入参数错误")

        cata = args[0]

        info_dict = {}
        info_dict["keywords"] = cata
        info_dict["desp"] = cata

        itemcatas=[];

        collection = self.db.project
        rslt = collection.find({"cata" : cata},{"title":1,"desp":1,"image":1,"brand":1})

        if 0 == rslt.count():
            self.render("e404_why.html",why="分类产品还不存在")
            return

        info_dict["brand"] = rslt[0]["brand"]

        for item in rslt:
            itemcatas.append(item)

        self.render("mobile/listCataItem.html",cataItem =itemcatas, infodict=info_dict)

       


class ListBrand(common.BaseHandle):
   def get(self, *args, **kwargs):
        if len(args) != 1:
            self.render("e404_why.html",why="输入参数错误")

        brand = args[0]

        info_dict = {}
        info_dict["keywords"] = brand
        info_dict["desp"] = brand

        collection = self.db.project
        rslt = collection.find({"brand" : brand},{"title":1,"desp":1,"image":1,"cata":1})
        for item in rslt:
            self.render("mobile/listBrandItem.html",newsItem =item, infodict=info_dict)
            return ;

        if 0 == rslt.count():
            self.render("e404_why.html",why="分类品牌还不存在")
