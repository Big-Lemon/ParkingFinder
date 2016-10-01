from tornado.web import RequestHandler


class HealthHandler(RequestHandler):

    def get(self):
        self.write('ok')

