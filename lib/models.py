#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  pymongo
import  datetime

class AdminMixin(object):
    def get_admin_by_email(self,email):
        collection = self.db.admins
        db_result = collection.find_one({"email":email})
        return db_result

    def get_admin_by_id(self, id):
        collection = self.db.admins
        db_result = collection.find_one({"_id":id})
        return  db_result

    # 超时的时候，调用
    def update_admin_salt(self,id ,token):
        collection = self.db.admins
        collection.update({"_id":id},{"$set":{"token":token}})

    # 登录后，设置，有效的时间
    def update_admin_token_time(self,id):
        now = datetime.datetime.utcnow()
        collection = self.db.admins
        collection.update({"_id":id},{"$set":{"token_time":now}})






