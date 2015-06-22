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

