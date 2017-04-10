import hcom
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.auth
import tornado.gen

from oauth2client import client, crypt
from pymongo import MongoClient
from tornado.options import define, options

CLIENT_ID = "284523515321-t0ugfeortsj0008gm63gs64153nm5omf.apps.googleusercontent.com"
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


class AuthHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.token = self.get_argument('token')
        posts = db.posts
        result = posts.find_one({'token': self.token})

        if result is None:
            raise tornado.web.HTTPError(400)



class CreateAccount(IndexHandler):
    def prepare(self):
        self.token = self.get_argument('token')
        posts = db.posts
        result = posts.find_one({'token': self.token})
        if not (result is None):
            raise tornado.web.HTTPError(400)

        try:
            self.idinfo = client.verify_id_token(self.token, CLIENT_ID)
            if self.idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError('Wrong issuer.')

        except crypt.AppIdentityError as e:
            raise tornado.web.HTTPError(400, reason=e)

    def post(self):
        email = self.idinfo['email']
        name = self.idinfo['name']

        posts = db.posts
        post_data = {
            'token': self.token,
            'name': name,
            'email': email
        }
        posts.insert_one(post_data)


class AllTypes(IndexHandler, AuthHandler):
    def get(self):
        try:
            #  Writes all the events as a JSON
            self.write({"status_code": 200, "status_message": self._reason, "list": hcom.h_com() + hcom.guide_conf() + hcom.vencity()})
        except:
            raise tornado.web.HTTPError(500)


class Hacks(IndexHandler, AuthHandler):
    def get(self):
        try:
            #  Writes all the hackathons as a JSON
            self.write({"status_code": 200, "status_message": self._reason, "list": hcom.h_com() + hcom.vencity()})
        except:
            raise tornado.web.HTTPError(500)


class Conf(IndexHandler, AuthHandler):
    def get(self):
        try:
            # Writes all the conferences as a JSON
            self.write({"status_code": 200, "status_message": self._reason, "list": hcom.guide_conf()})
        except:
            raise tornado.web.HTTPError(500)


if __name__ == "__main__":
    mclient = MongoClient()
    db = mclient['users']
    x = db.posts
    x.insert_one({'token': 'abc', 'email': 'sam@a.com', 'name': 'samtan'})
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
            (r"/create", AuthHandler)
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
