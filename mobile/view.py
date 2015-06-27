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
        if len(args) < 1 :
            self.redirect("/")

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
            self.redirect("/")

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



