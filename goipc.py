#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#


import  os.path
import  getopt

import  tornado
import  tornado.auth
import  tornado.httpserver
import  tornado.ioloop
import  tornado.web as Web
import  tornado.options
import  pymongo

from tornado.options import define, options
from  tornado.log import  access_log

import sys
sys.path.append("/home/songchengkui/NewWebSite/V2GoIPC")

import admin.admin as adminuser
import admin.category as category
import admin.product as product
import admin.usandnews as News

from lib import common, ueditorhander, upLoadFile


define("port",default=20000,help="run on the given port", type=int)

WebPort = 0



class IndexHandler(common.BaseHandle):
    def get(self, *args, **kwargs):
        self.render("index.html",lorm="xxxxx")




class Application(tornado.web.Application):
    def  __init__(self):
        handlers = [
            (r"/admin/ueditorHander", ueditorhander.UEditorManager),
            (r"/admin/uploadimage", upLoadFile.UpLoadImage),
            (r"/ueditor",product.testUeditor),

            (r"/",IndexHandler),
            (r"^/admin.?$", adminuser.AdminIndex),
            (r"^/QAdmin/login.?$", adminuser.AdminLogin),
            (r"^/admin/logout.?$", adminuser.AdminLogout),

            (r"^/admin/category.?$" , category.listCategory),
            (r"^/admin/addbrand.?$",category.AddBrandName),
            (r"^/admin/deleteBrand.?$", category.deleteBrand) ,
            (r"^/admin/editBrand.?$", category.editBrand) ,
            (r"^/admin/addCata.?$", category.AddCataName) ,
            (r"^/admin/editCata.?$", category.editCataName) ,
            (r"^/admin/deleCata.?$", category.deleteCataName) ,
            (r"^/admin/getCatasByBrand.?$", category.getCatalistByBrand) ,


            (r"^/admin/addProduct.?$", product.addProduct) ,
            (r"^/admin/listProduct.?$", product.listProduct) ,
            (r"^/admin/editProduct.?$", product.editProduct) ,
            (r"^/admin/deleProduct.?$", product.deleProduct) ,

            (r"^/admin/listNews.?$", News.ListNews) ,
            (r"^/admin/addNew.?$", News.AddNews) ,
            (r"^/admin/editNew.?$", News.editNew) ,
            (r"^/admin/deleNew.?$", News.deleteNew) ,

            #(r"^$",IndexHandler),
        ]
        setting =dict (
            blog_title=u"北京国信智维科技有限公司",
            blog_nav_First=u"主页",
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            xsrf_cookires=True,
            cookie_secret="I321Qu+ZacEL3uMlRPgVkrmmzn1FvKvYhP3Lobc",
            login_url="/auth/login" ,
            debug=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self,handlers, **setting)
        self.db = pymongo.MongoClient('localhost',27017).goipc



class MyErrorHandler(Web.RequestHandler):
    """Generates an error response with ``status_code`` for all requests."""
    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        access_log.error("[MyErrorHandler] %d" % self._status_code )
        #if self._status_code == 404:
        #   return self.render("e404.html")

        raise Web.HTTPError(self._status_code)

    def check_xsrf_cookie(self):
        # POSTs to an ErrorHandler don't actually have side effects,
        # so we don't need to check the xsrf token.  This allows POSTs
        # to the wrong url to return a 404 instead of 403.
        pass




def main():
    tornado.options.parse_command_line()
    #tornado.web.ErrorHandler = MyErrorHandler
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    # opts, args = getopt.getopt(sys.argv[1:], "hp:")
    # for op, value in opts:
    #     if op == "-p":
    #         WebPort = int(value)
    #     elif op == "-h":
    #         print "python goipc.py -p 20000"
    #         sys.exit()
    #     else:
    #         print "python goipc.py -p 20000"
    #         sys.exit()

    # if WebPort == 0 :
    #     print "python goipc.py -p 20000"
    #     sys.exit()
    # else :
    #     main()

    main()



