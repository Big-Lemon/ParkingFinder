from ParkingFinder.entities.entity import Entity
from ParkingFinder.mappers import Mapper
from ParkingFinder.entities.available_parking_space import AvailableParkingSpace
from ParkingFinder.tables.available_parking_space_pool import AvailableParkingSpacePool

class AvailableParkingSpaceMapper(Mapper):
    _ENTITY = AvailableParkingSpace
    _MODEL = AvailableParkingSpacePool

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
            'updated_at': record.updated_at,
        }
        print record.is_active
        if record.is_active == 1:
            params.update({'is_active': True})
        else:
            params.update({'is_active': False})
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
            'longitude': entity.location.longitude,
            'latitude': entity.location.latitude,
            'is_active': entity.is_active,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at,
        }
        if entity.location.level:
            params.update({'level': entity.location.level})
        if entity.location.location:
            params.update({'location': entity.location.location})
        return cls._MODEL(**params)
