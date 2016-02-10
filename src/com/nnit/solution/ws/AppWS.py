import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from com.nnit.solution.service import UserService
from com.nnit.solution.redisdao import user_redis_dao
from tornado.options import define, options

define("port", default=8889, help="run on the given port", type=int)
class WSHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="cellphone">'
                   '<input type="submit" value="Login">'
                   '</form></body></html>')

    def post(self):
        self.write('<html><body>login in successfully!</body></html>')
        userService = UserService.UserService()
        try:
            self.write(self.get_argument('cellphone'))
            if userService.login(self.get_argument('cellphone')):
                self.write('<html><body>login in successfully!</body></html>')
            else:
                self.write('<html><body>login fail!</body></html>')
        except user_redis_dao.UserNotExistException as err:
            print("UserNotExistException occure!")
            self.write("UserNotExistException occure!")



class niubi(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("xiaorui.cc niubi'id is " + story_id)


"""
shoppingmall的RESTful接口
"""
class shoppingmall(tornado.web.RequestHandler):

    @get(_path="/shops",shops=mediatypes.APPLICATION_JSON)
    def fetchHotShops(self, shops):
        pass;

"""
用户登录
"""
class UserLogin(tornado.web.RedirectHandler):
    def get(self):
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="cellphone">'
                   '<input type="submit" value="Login">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("This is the first WS over Python " + self.get_argument("cellphone"))

"""
根据ID得到用户信息
"""
class getUserById(tornado.web.RedirectHandler):
    def get(self):
        userServcie = UserService()


application = tornado.web.Application([
    (r"/", WSHandler),
    (r"/niubi/([0-9]+)", niubi),
])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", WSHandler),
        (r"/niubi/([0-9]+)", niubi),
        (r"/shoppingmall/shops")
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
