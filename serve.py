from clay import config
from tornado import ioloop
from tornado.httpserver import HTTPServer

from ParkingFinder.handlers.app import app

if __name__ == '__main__':
    server = HTTPServer(app)
    server.listen(config.get('server.port'))
    print 'server is listening on port ' + str(config.get('server.port'))
    ioloop.IOLoop.current().start()
