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
        info_dict= {}
        info_dict["keywords"] = "研华工控机,研华原装工控机,西门子工控机,研祥工控机,凌华工控机,华北工控机,"
        info_dict["desp"] = "北京国信智维科技有限公司一直致力于PC-based工控机的推广与应用事业，" \
                            "经过长期的努力，现已成为研华工控机金牌代理商，西门子工控机一级经销商，研祥工控机核心经销商，" \
                            "华北工控机金牌代理商，凌华工控机核心经销商等，欢迎广大客户来电与我公司洽谈"
        self.render("mobile/index.html", infodict=info_dict)