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
import  tornado.web
import  tornado.options

import  common
import  admin

from tornado.options import define, options

define("port",default=8888,help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")





class IndexHandler(common.BaseHandle):
    def get(self, *args, **kwargs):
        self.render("index.html",lorm="xxxxx")



class TestFullIndex(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return  self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

class Application(tornado.web.Application):
    def  __init__(self):
        handlers = [
            (r"/",IndexHandler),
            (r"/v2/test",TestFullIndex),
            (r"/admin", admin.AdminIndex)
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


def main():
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()




