from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    @property
    def url(self):
        return (
            "%s://%s%s" %
            (self.request.protocol,
             self.request.host,
             self.request.uri
             )
        )
