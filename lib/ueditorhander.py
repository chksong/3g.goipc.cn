#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
#   配合百度的的ueditor 控件，做后台文件的上传

import tornado
import tornado.web
import os.path
import json
import re
import datetime
from common import BaseHandle

ueditor_json = dict()

def loadUeditorJson():
    global  ueditor_json
    try:
        with open(u'static/ueditor/python/config.json') as f:
            context = f.read()
            #删除`/**/`注释
            text = re.sub("\/\*[\s\S]+?\*\/" , '' ,context)
            ueditor_json = json.loads(text)
    except :
        ueditor_json = {}


class UEditorManager(BaseHandle):
    def get(self):
        action = self.get_argument("action")
        if action=="config":
            if 0 == len(ueditor_json):
                loadUeditorJson()
                print("UEditorManager configure file " , ueditor_json)

            self.write(ueditor_json)

    def post(self):
        action = self.get_argument("action")
        if action == "uploadimage":
            config = {
                'pathFormat':ueditor_json['imagePathFormat'],
                'maxSize':ueditor_json['imageMaxSize'],
                'allowFiles':ueditor_json['imageAllowFiles']
            }
            fieldname = ueditor_json['imageFieldName']
            self.uploadImage(fieldname,config)
        elif action == "uploadfile":
            config = {
                'pathFormat':ueditor_json['filePathFormat'] ,
                'maxSize':ueditor_json['fileMaxSize'],
                'allowFiles':ueditor_json['fileAllowFiles']
            }
            fieldname = ueditor_json['fileFieldName']
            self.uploadImage(fieldname,config)
        elif action == "uploadvideo":
            config = {
                'pathFormat':ueditor_json['videoPathFormat'] ,
                'maxSize':ueditor_json['videoMaxSize'],
                'allowFiles':ueditor_json['videoAllowFiles']
            }
            fieldname = ueditor_json['fileFieldName']
            self.uploadImage(fieldname,config)
        elif action == "uploadscrawl":
            pass


    def uploadImage(self, filedname , configjson):
        upfile = self.request.files[filedname]
        if upfile:
            filename = upfile[0]['filename']
            now=datetime.datetime.now()
            save_path=configjson['pathFormat'] % (now.year,now.month,now.day)
            if not os.path.exists(save_path):
                os.makedirs (save_path)

            rand_str = u'%06d-%s' %(now.microsecond ,filename)
            save_name =u'{}{}'.format(save_path,rand_str)

            fout = open(save_name, 'wb')
            fout.write(upfile[0]['body'])
            fout.close()

            result = {
              "state": "SUCCESS",
              "url": save_name,
              "title": filename,
              "original": filename ,
            }
            self.write(result)

    def uploadFile(self, filedname ,configson):
        pass