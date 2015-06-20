#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2015 chksong
#  chksong@qq.com
#
#  移动站点的 后台逻辑
#  2015-6-10 日


from  tornado.log import  access_log
import  logging
import  re

import  tornado
import  tornado.escape


from lib import common

class index (common.BaseHandle):
    def get(self, *args, **kwargs):
        self.render("mobile/index.html")
