from ParkingFinder.tables.parking_lot import ParkingLot
from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.mappers import Mapper


class ParkingSpaceMapper(Mapper):
    _ENTITY = ParkingSpace
    _MODEL = ParkingLot

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
            'plate': record.plate,
            'location': location,
            'created_at': record.created_at,
        }

        return params

    @staticmethod
    def _to_record(entity):

        params = {
            'plate': entity.plate,
            'latitude': entity.location.latitude,
            'longitude': entity.location.longitude,
        }

        if entity.location.level:
            params.update({'level': entity.location.level})
        if entity.location.location:
            params.update({'address': entity.location.location})

        return params

    @classmethod
    def _to_model(cls, entity):
        params = {
            'plate': entity.plate,
            'latitude': entity.location.latitude,
            'longitude': entity.location.longitude,
            'created_at': entity.created_at,
        }
        if entity.location.level:
            params.update({'level': entity.location.level})
        if entity.location.location:
            params.update({'location': entity.location.location})

        return cls._MODEL(**params)

