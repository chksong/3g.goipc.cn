#!/usr/bin/env python
#-*-coding:utf-8-*-
# Copyright 2009 chksong
#  chksong@qq.com
#


import  os.path
import  re
import  tornado
import  tornado.auth
import  tornado.httpserver
import  tornado.ioloop
import  tornado.web
import  tornado.options

from tornado.options import define, options

define("port",default=8888,help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")



class BaseHandle(tornado.web.RequestHandler):
    @property
    def db(self):
        return  self.application.db

class IndexHandler(BaseHandle):
    def get(self, *args, **kwargs):
        self.render("index.html",lorm="xxxxx")


class Application(tornado.web.Application):
    def  __init__(self):
        handlers = [
            (r"/",IndexHandler),
        ]
        setting =dict (
            blog_title=u"周易App",
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            xsrf_cookires=True,
            cookie_secret="akdhdoudisfppplkjiijjji",
            login_url="/auth/login" ,
            debug=True,
        )
        tornado.web.Application.__init__(self,handlers, **setting)


def main():
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()




