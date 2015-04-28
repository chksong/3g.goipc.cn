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
from common import BaseHandle

ueditor_json = dict()

def loadUeditorJson():
    global  ueditor_json
    with open('static/ueditor/python/config.json') as f:
        context = f.read()
        text = re.sub("/\*[\s\S]+?\*/" , '' ,context)
        ueditor_json = json.loads(text)

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
            self.uploadimage()



    def uploadimage(self):
        upfile = self.request.files['upfile']
        if upfile:
            filename = upfile[0]['filename']
            #path_file = ueditor_json['imagePathFormat']
            path_file = "static/upload/test.png"


            str_path = path_file[0:path_file.rfind('/')]
            if not os.path.exists(str_path):
                os.mkdir(str_path)

            f_out = open('static/upload/test.png', 'wb')
            nums = f_out.write(upfile[0]['body'])
            print nums , len(upfile[0]['body'])

            f_out.close()

            print( filename, path_file)



