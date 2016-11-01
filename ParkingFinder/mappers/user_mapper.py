from datetime import datetime

from ParkingFinder.entities.user import User
from ParkingFinder.mappers import Mapper
from ParkingFinder.tables.user import Users


class UserMapper(Mapper):
    _ENTITY = User
    _MODEL = Users

    @staticmethod
    def _build_map(record):
        params = {
            'user_id': record.user_id,
            'first_name': record.first_name,
            'last_name': record.last_name,
            'profile_picture_url': record.profile_picture_url,
        }
        if record.activated_vehicle:
            params.update({'activated_vehicle': record.activated_vehicle})
        # TODO if record has a list of vehicles, use VehicleMapper.to_entity
        # to map them into params['owned_vehicles']

        return params

    @staticmethod
    def _to_record(entity):
        params = entity.to_primitive()

        return params

    @classmethod
    def _to_model(cls, entity):
        params = entity.to_primitive()
        del params['owned_vehicles']

        return cls._MODEL(**params)

