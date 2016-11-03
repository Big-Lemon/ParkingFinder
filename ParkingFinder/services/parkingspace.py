from sqlalchemy.orm.exc import NoResultFound
from schematics.exceptions import ValidationError
from tornado.gen import coroutine, Return

from ParkingFinder.base.errors import (
    NotFound,
    InvalidEntity,
)
from ParkingFinder.repositories.real_time_repository import RealTimeRepository

from clay import config

logger = config.get_logger('parkingspace')


class ParkingSpaceService(object):

	@staticmethod
	@coroutine
	def update_real_time_location(realtime):
		"""
		update the real time location for both waiting user
		and request user.

		:param RealTime realtime:
		:return RealTime
	    """
		try:
			realtime.validate()
		except ValidationError:
			raise InvalidEntity

		_realtime = yield RealTimeRepository.upsert(realtime)

		raise Return(_realtime)

	@staticmethod
	@coroutine
	def initialize_waiting_user_location(user_id):
		"""
		initialize waiting user location
		since waiting user doesn't know who gonna 
		be his pair so he will fecth to see who is his pair
		for 5 mins

		:param  String user_id
		:return RealTime 
		"""
		try:
			_realtime = yield RealTimeRepository.read_one(user_id)
			raise Return(_realtime)

		except NoResultFound:
			logger.info(user_id + ': no one match this location')
			raise NotFound




