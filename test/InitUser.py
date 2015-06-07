#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015-3-28 chksong
#  chksong@qq.com
#
# 测试 mongdb

import sys


import  pymongo
import  pymongo.collection
import  datetime

sys.path.append("/home/songchengkui/NewWebSite/V2Goipc")

from  lib  import  crypto

print datetime.datetime.utcnow()


con = pymongo.MongoClient('localhost',27017)
db = con.goipc
collection = db.admins

def testAddMongDB():
    try:
        token = crypto.get_random_string()
        enpass = crypto.PasswordCrypto.get_encrypted("fanfan120725")

        now = datetime.datetime.utcnow()

        collection.insert({"name":"songck","passwd": enpass,"email":"chksong@goipc.cn","token":token ,"token_time":now})
    except Exception ,e:
        print '**********' ,e
    else:
        print 'No exception was raised.'

def updateMongDB():

    post = collection.find_one({"name":"songck"})
    print 'post["token_time"]' , post["token_time"]

    now_diff = datetime.datetime.utcnow() - post["token_time"]
    print 'now_diff' , now_diff

    time_out = datetime.timedelta(hours =1 )
    if now_diff > time_out:
        print "证书超时。"

    db_get = collection.find_one({"_id":post["_id"]})
    print( db_get)
    print db_get["_id"]


    #collection.update({"_id":post["_id"]},{"$set":{"passwd":"22222"}})

testAddMongDB()
#updateMongDB()











