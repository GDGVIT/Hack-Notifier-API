import hcom
import os
import tornado.auth
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options


define("port", default=8000, help="runs on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.write({"status_code": status_code, "status_message": self._reason})
        elif status_code == 500:
            self.write({"status_code": status_code, "status_message": "Scraping Error"})
        elif status_code == 400:
            self.write({"status_code": status_code, "status_message": self._reason})


class ErrorHandler(tornado.web.ErrorHandler, IndexHandler):
    pass


class AllTypes(IndexHandler):
    async def get(self):
        try:
            #  Writes all the events as a JSON
            self.write(
                {
                    "status_code": 200,
                    "status_message": self._reason,
                    "list": hcom.h_com() + hcom.guide_conf() + hcom.vencity()
                }
            )
        except:
            raise tornado.web.HTTPError(500)


class Hacks(IndexHandler):
    async def get(self):
        try:
            #  Writes all the hackathons as a JSON
            self.write(
                {
                    "status_code": 200,
                    "status_message": self._reason,
                    "list": hcom.h_com() + hcom.vencity()
                }
            )

        except:
            raise tornado.web.HTTPError(500)


class Conf(IndexHandler):
    async def get(self):
        result,reason = await hcom.guide_conf()
        if result == []:
            self.write(
                {
                    "status_code": 500,
                    "status_message": reason,
                    "list": []
                }
            )
        else:
            # Writes all the conferences as a JSON
            self.write(
                {
                    "status_code": 200,
                    "status_message": self._reason,
                    "list": result
                }
            )


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        'default_handler_class': ErrorHandler,
        'default_handler_args': dict(status_code=404)
    }
    app = tornado.web.Application(
        handlers=[
            (r"/", AllTypes),
            (r"/hackathons", Hacks),
            (r"/conferences", Conf),
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(os.environ.get("PORT",options.port))
    tornado.ioloop.IOLoop.instance().start()
