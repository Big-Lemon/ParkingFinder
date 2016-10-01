from tornado.web import Application

from ParkingFinder.handlers import HealthHandler

app = Application([
    (r'/health', HealthHandler)
])
