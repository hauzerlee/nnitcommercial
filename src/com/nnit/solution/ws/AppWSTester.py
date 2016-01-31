import tornado.ioloop
import tornado.web
import json


class hello(tornado.web.RequestHandler):
    def get(self):
        self.write('Testing WS on Python')


class add(tornado.web.RequestHandler):
    def post(self):
        res = Add(json.loads(self.request.body))
        self.write(json.dumps(res))


def Add(input):
    sum = input['num1'] + input['num2']
    result = {}
    result['sum'] = sum
    return result


application = tornado.web.Application([
    (r"/", hello),
    (r"/add", add),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
