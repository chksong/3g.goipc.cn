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


class AddNews(common.BaseHandle):
     def get(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        self.render("admin/newsadd.html",admin_user=admin_user)

     def post(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        title = self.get_argument("title")
        cata =  self.get_argument("cata")

        collection = self.db.NEWS
        rslt = collection.find({"title":title ,"cata" : cata}, {"name":1})
        if rslt.count():
            get_dict = {
                "content":"新闻名称已经存在",
                "state":-1 ,
            }
            self.write(get_dict)
            return

        keywords= self.get_argument("keywords")
        desp= self.get_argument("desp")
        context = self.get_argument("context")
        arrKeyWord = keywords.split(",")

        collection.insert({"title":title,   "cata":cata ,"keywords":arrKeyWord ,
                           "desp":desp,  "context":context})

        self.write({"content":"新闻添加成功", "state":1 })


class ListNews(common.BaseHandle):
    def get(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        arr_news = []
        collection = self.db.NEWS
        rslt = collection.find({}, {"_id":1 ,"title":1 ,"brand":1 , "cata":1})
        for row_item in rslt:
            item={}
            item["id"] = str(row_item["_id"])
            item["title"] = row_item["title"]
            item["cata"] = row_item["cata"]

            arr_news.append(item)

        print arr_news
        self.render("admin/newslist.html",admin_user=admin_user ,arrNews= arr_news)

class deleteNew(common.BaseHandle):
    def post(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        newid =self.get_argument("pid")

        collection = self.db.NEWS
        db_result = collection.remove({"_id":ObjectId(newid)})
        self.write({"content":"删除成功", "state":1})


class editNew(common.BaseHandle):
    def get(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return


        pid =self.get_argument("pid")
        collection = self.db.NEWS
        rslt = collection.find({"_id":ObjectId(pid) })

        for item in rslt :
            separator = ","
            strKeywords = separator.join(item["keywords"])
            item["keywords"]=strKeywords

            print item["keywords"]
            self.render("admin/newsedit.html" ,admin_user=admin_user ,newsItem =item)

    def post(self, *args, **kwargs):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        pid = self.get_argument("pid")
        title = self.get_argument("title")
        cata =  self.get_argument("cata")

        keywords= self.get_argument("keywords")
        desp= self.get_argument("desp")
        context = self.get_argument("context")
        arrKeyWord = keywords.split(",")

        collection = self.db.NEWS
        collection.update({"_id":ObjectId(pid)},{"$set" :{"title":title,   "cata":cata ,"keywords":arrKeyWord ,
                           "desp":desp,  "context":context}})

        self.write({"content":"修改新闻活或者公司简介成功", "state":1 })