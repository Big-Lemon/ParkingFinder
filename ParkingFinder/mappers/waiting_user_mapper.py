from ParkingFinder.mappers import Mapper
from ParkingFinder.entities.waiting_user import WaitingUser
from ParkingFinder.tables.waiting_users import WaitingUsers


class WaitingUserMapper(Mapper):
    _ENTITY = WaitingUser
    _MODEL = WaitingUsers

    @staticmethod
    def _build_map(record):
        location = {
            'longitude': record['longitude'],
            'latitude': record['latitude'],
        }
        level = record.get('level', None)
        address = record.get('address', None)
        if level:
            location['level'] = level
        if address:
            location['address'] = address

        params = {
            'user_id': record['user_id'],
            'location': location,
            'is_active': record['is_active'],
            'created_at': record['created_at'],
        }

        return params

    @staticmethod
    def _to_record(entity):
        record = {
            'user_id': entity.user_id,
            'longitude': entity.location.longitude,
            'latitude': entity.location.latitude,
            'created_at': str(entity.created_at)
        }
        if entity.location.location:
            record['address'] = entity.location.location
        if entity.location.level:
            record['level'] = entity.location.level
        return record

    @classmethod
    def _to_model(cls, entity):
        params = {
            'user_id': entity.user_id,
            'longitude': entity.location.longitude,
            'latitude': entity.location.latitude,
            'created_at': entity.created_at,
        }
        if entity.location.level:
            params.update({'level': entity.location.level})
        if entity.location.location:
            params.update({'location': entity.location.location})
        return cls._MODEL(**params)