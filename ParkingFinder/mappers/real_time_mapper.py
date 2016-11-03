from datetime import datetime

from ParkingFinder.entities.real_time import RealTime
from ParkingFinder.mappers import Mapper
from ParkingFinder.tables.real_time import RealTimes


class RealTimeMapper(Mapper):
    _ENTITY = RealTime
    _MODEL = RealTimes

    @staticmethod
    def _build_map(record):
        params = {
            'waiting_user_id': record.waiting_user_id,
            'waiting_user_latitude': record.waiting_user_latitude,
            'waiting_user_longitude': record.waiting_user_longitude,
            'request_user_id': record.request_user_id,
            'request_user_latitude': record.request_user_latitude,
            'request_user_longitude': record.request_user_longitude,
            'created_at': record.created_at,
        }

        return params

    @staticmethod
    def _to_record(entity):
        params = entity.to_primitive()

        return params

    @classmethod
    def _to_model(cls, entity):
        params = entity.to_primitive()

        return cls._MODEL(**params)

