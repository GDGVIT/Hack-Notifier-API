import hcom
import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

define("port", default=8000, help="runs on the given port", type=int)


class AllTypes(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(hcom.h_com() + hcom.guide_conf() + hcom.vencity()))


class hacks(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(hcom.h_com() + hcom.vencity()))


class conf(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(hcom.guide_conf()))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", AllTypes),
            (r"/hackathons", hacks),
            (r"/conferences", conf)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
