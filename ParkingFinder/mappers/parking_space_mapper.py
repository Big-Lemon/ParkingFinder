from ParkingFinder.tables.parking_lot import ParkingLot
from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.mappers import Mapper


class ParkingSpaceMapper(Mapper):
    _ENTITY = ParkingSpace
    _MODEL = ParkingLot

    @staticmethod
    def _build_map(record):
        params = {
            'plate': record.plate,
            'latitude': record.latitude,
            'longitude': record.longitude,
            'created_at': record.created_at,
        }
        if record.level:
            params.update({'level': record.level})
        if record.location:
            params.update({'location': record.location})

        return params

    @staticmethod
    def _to_record(entity):

        params = {
            'token:' entity.plate,
            'latitude': entity.latitude,
            'longitude': entity.longitude,
        }

        if entity.level:
            params.update({'level': entity.level})
        if entity.description:
            params.update({'description': entity.description})

        return params

    @classmethod
    def _to_model(cls, entity):
        params = {
            'plate': entity.plate,
            'latitude': entity.latitude,
            'longitude': entity.longitude,
            'created_at': entity.created_at,
        }
        if entity.level:
            params.update({'level': entity.level})
        if entity.location:
            params.update({'location': entity.location})

        return cls._MODEL(**params)

