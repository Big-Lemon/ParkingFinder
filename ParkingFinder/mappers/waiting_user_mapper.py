from ParkingFinder.entities.entity import Entity
from ParkingFinder.mappers import Mapper
from ParkingFinder.entities.waiting_user import WaitingUser
from ParkingFinder.tables.waiting_users import WaitingUsers

class WaitingUserMapper(Mapper):
    _ENTITY = WaitingUser
    _MODEL = WaitingUsers

    @staticmethod
    def _build_map(record):
        location = {
            'longitude': record.longitude,
            'latitude': record.latitude,
        }
        if record.level:
            location.update({'level': record.level})
        if record.location:
            location.update({'location': record.location})

        params = {
            'user_id': record.user_id,
            'location': location,
            'is_active': record.is_active,
            'created_at': record.created_at,
        }

        return params


    @staticmethod
    def _to_record(entity):
        return entity.to_primitive()


    @classmethod
    def _to_model(cls, entity):
        params = {
            'user_id': entity.user_id,
            'longitude': entity.location.longitude,
            'latitude': entity.location.latitude,
            'is_active': entity.is_active,
            'created_at': entity.created_at,
        }
        if entity.location.level:
            params.update({'level': entity.location.level})
        if entity.location.location:
            params.update({'location': entity.location.location})
        return cls._MODEL(**params)