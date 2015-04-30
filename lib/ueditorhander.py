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

class GetUpFiles(BaseHandle):
    def get(self):

        self.wirte("")
        pass


class UEditorManager(BaseHandle):
    def get(self):
        if 0 == len(ueditor_json):
                loadUeditorJson()

        action = self.get_argument("action")
        if action=="config":
            print("get configure json " , ueditor_json)
            self.write(ueditor_json)

        elif action == "listimage":
            path = ueditor_json['imageManagerListPath']
            self.listImage(path)
        elif action == "listfile" :
            path = ueditor_json['fileManagerListPath']
            self.listImage(path)


    def post(self):
        if 0 == len(ueditor_json):
             loadUeditorJson()

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
            ## 检验扩展类型
            str_ext = filename[filename.rfind('.'):]
            if not (str_ext in configjson['allowFiles']):
                 self.write({"state" :'文件类型不允许'})
                 return

            ##创建文件的路径
            now=datetime.datetime.now()
            save_path=configjson['pathFormat'] % (now.year,now.month,now.day)
            if not os.path.exists(save_path):
                try:
                    os.makedirs (save_path)
                except Exception as oserr :
                    self.write({"state" : str(oserr)})
                    return

            ##构造文件名字
            rand_str = u'%06d-%s' %(now.microsecond ,filename)
            save_name =u'{}{}'.format(save_path,rand_str)
            url_name = u'/{}'.format(save_name)

            ##保存文件
            try:
                fout = open(save_name, 'wb')
                fout.write(upfile[0]['body'])
                fout.close()
            except Exception as oserr :
                self.write({"state" : str(oserr)})
                return

            ##检查文件长度 & 删除该文件
            file_len = os.path.getsize(save_name)
            if file_len >  configjson['maxSize'] :
                self.write({"state" : '文件大小超出网站限制'})
                os.remove(save_name)
                return


            ##保存文件成功
            result = {
              "state": "SUCCESS",
              "url": url_name,
              "title": filename,
              "original": filename ,
            }
            self.write(result)

    def listImage(self ,filePath ):
         #GET {"action": "listimage", "start": 0, "size": 20}
        start = int(self.get_argument("start"))
        size =  int (self.get_argument("size"))
        i_start  = 0
        i_size   = 0
        urls = []

        try:
            lsdir = os.listdir(filePath)
            for d in lsdir:
                in_dir = u'{}{}'.format(filePath,d)
                filelist = os.listdir(in_dir)
                for f in filelist:
                    #f_name = u'{}{}/{}'.format(filePath,d,f)
                    f_name = u'{}/{}'.format(d,f)
                    if i_start >= start and i_size <size :
                        i_size += 1
                        f_name_utf8 =  f_name.encode('utf-8')
                     #   print f_name , f_name_utf8
                        urls.append({'url':f_name_utf8})

                    #技术一共有多少个文件
                    i_start += 1

        except Exception as oserr :
            self.write({"state" : str(oserr)})
            return

        result = {
            "state": "SUCCESS",
            "list": urls,
            "start": start ,
            "total": i_start
        }
        self.write(result)
