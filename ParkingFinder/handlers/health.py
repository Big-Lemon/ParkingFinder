from tornado.web import RequestHandler


class HealthHandler(RequestHandler):

    def get(self):
        self.set_status(200)
        self.write('ok')

