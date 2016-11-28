from ParkingFinder.mappers import Mapper
from ParkingFinder.entities.waiting_user import WaitingUser


class WaitingUserMapper(Mapper):
    _ENTITY = WaitingUser

    @staticmethod
    def _build_map(record):
        location = {
            'longitude': float(record['longitude']),
            'latitude': float(record['latitude']),
        }
        level = record.get('level', None)
        address = record.get('address', None)
        if level:
            location['level'] = level
        if address:
            location['location'] = address

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
