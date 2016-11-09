from ParkingFinder.tables.check_in_parking_space import CheckInParkingSpace
from ParkingFinder.tables.check_out_parking_space import CheckOutParkingSpace
from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.mappers import Mapper


class ParkingSpaceMapper(Mapper):
    _ENTITY = ParkingSpace

    @staticmethod
    def _build_map(record):
        params = {
            'user_id': record.user_id,
            'latitude': record.latitude,
            'longitude': record.longitude,
            'created_at': record.created_at,
        }
        if record.level:
            params.update({'level': record.level})
        if record.description:
            params.update({'description': record.description})

        return params

    @staticmethod
    def _to_record(entity):
        params = entity.to_primitive()

        return params


class CheckInParkingSpaceMapper(ParkingSpaceMapper):
    _MODEL = CheckInParkingSpace

    @classmethod
    def _to_model(cls, entity):
        return cls._MODEL(**{
            'user_id': entity.user_id,
            'latitude': entity.latitude,
            'longitude': entity.longitude,
            'created_at': entity.created_at,
        })


class CheckOutParkingSpaceMapper(ParkingSpaceMapper):
    _MODEL = CheckOutParkingSpace

    @classmethod
    def _to_model(cls, entity):
        return cls._MODEL(**{
            'user_id': entity.user_id,
            'latitude': entity.latitude,
            'longitude': entity.longitude,
            'created_at': entity.created_at,
        })
