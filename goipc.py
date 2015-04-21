#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#


import  os.path
import  tornado
import  tornado.auth
import  tornado.httpserver
import  tornado.ioloop
import  tornado.web as Web
import  tornado.options
import  pymongo
from tornado.options import define, options
from  tornado.log import  access_log


import admin.admin as adminuser
import admin.category as category

from lib import common


define("port",default=8888,help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")





class IndexHandler(common.BaseHandle):
    def get(self, *args, **kwargs):
        self.render("index.html",lorm="xxxxx")




class Application(tornado.web.Application):
    def  __init__(self):
        handlers = [

            (r"/",IndexHandler),

            (r"^/admin.?$", adminuser.AdminIndex),
            (r"/admin/login.?$", adminuser.AdminLogin),
            (r"^/admin/logout.?$", adminuser.AdminLogout),
            (r"^/admin/category.?$" , category.listCategory),
            #(r"^$",IndexHandler),
        ]
        setting =dict (
            blog_title=u"北京国信智维科技有限公司",
            blog_nav_First=u"主页",
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            xsrf_cookires=True,
            cookie_secret="akdhdoudisfppplkjiijjji",
            login_url="/auth/login" ,
            debug=True,
        )
        tornado.web.Application.__init__(self,handlers, **setting)
        self.db = pymongo.Connection('localhost',27017).goipc


class MyErrorHandler(Web.RequestHandler):
    """Generates an error response with ``status_code`` for all requests."""
    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        access_log.error("[MyErrorHandler] %d" % self._status_code )
        if self._status_code == 404:
            return self.render("e404.html")

       # raise Web.HTTPError(self._status_code)

    def check_xsrf_cookie(self):
        # POSTs to an ErrorHandler don't actually have side effects,
        # so we don't need to check the xsrf token.  This allows POSTs
        # to the wrong url to return a 404 instead of 403.
        pass




def main():
    tornado.options.parse_command_line()
    tornado.web.ErrorHandler = MyErrorHandler
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()




