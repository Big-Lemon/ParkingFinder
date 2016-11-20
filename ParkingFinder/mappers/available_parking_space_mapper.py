from datetime import datetime, timedelta

from clay import config

from ParkingFinder.entities.entity import Entity
from ParkingFinder.mappers import Mapper
from ParkingFinder.entities.available_parking_space import AvailableParkingSpace
from ParkingFinder.tables.available_parking_space_pool import AvailableParkingSpacePool

WAITING_TIME = config.get('available_parking.waiting_duration')


class AvailableParkingSpaceMapper(Mapper):
    _ENTITY = AvailableParkingSpace
    _MODEL = AvailableParkingSpacePool

    @staticmethod
    def _build_map(record, *args, **params):
        assert record.get('is_active', None)

        location = {
            'longitude': record['longitude'],
            'latitude': record['latitude'],
        }
        address = record.get('address', None)
        level = record.get('level', None)

        if address:
            location['location'] = address
        if level:
            location['level'] = level



        params = {
            'plate': record['plate'],
            'location': location,
            'is_active': record['is_active'],
            'expired_at': record['expired_at'],
            'distance': record.get('distance', None)
        }
        return params

    @staticmethod
    def _to_record(entity):
        params = {
            'plate': entity.plate,
            'latitude': entity.location.latitude,
            'longitude': entity.location.longitude,
            'expired_at': str(entity.expired_at)
        }
        if entity.location.location:
            params['address'] = entity.location.location
        if entity.location.level:
            params['level'] = entity.location.level

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
