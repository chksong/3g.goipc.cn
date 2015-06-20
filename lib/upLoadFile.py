#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
##  上传文件图片


import tornado
import tornado.web
import os.path
import json
import re
import datetime
from common import BaseHandle


# /* 上传文件配置 */
#     "fileActionName": "uploadfile", /* controller里,执行上传视频的action名称 */
#     "fileFieldName": "upfile", /* 提交的文件表单名称 */
#     "filePathFormat": "static/upload/file/%04d-%02d-%02d/", /* 上传保存路径,可以自定义保存路径和文件名格式 */
#     "fileUrlPrefix": "", /* 文件访问路径前缀 */
#     "fileMaxSize": 5120000, /* 上传大小限制，单位B，默认5MB */
#     "fileAllowFiles": [
#         ".png", ".jpg", ".jpeg", ".gif", ".bmp",
#         ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
#         ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
#         ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
#         ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
#     ], /* 上传文件格式显示 */



class UpLoadImage (BaseHandle):
    def post(self):
        admin_user = self.get_admin_user()
        if  not admin_user:
            self.redirect("/")
            return

        config = {
            'pathFormat':"static/upload/file/%04d-%02d-%02d/" ,
            'maxSize':2048000,
            'allowFiles': [
                ".png", ".jpg", ".jpeg", ".gif", ".bmp",
                 ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
                  ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
                 ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
                 ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml" ],
            }
        fieldname = "image"
        self.uploadImage(fieldname,config)


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