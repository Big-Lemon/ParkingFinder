from ParkingFinder.entities.real_time_location import RealTimeLocation
from ParkingFinder.mappers import Mapper


class RealTimeLocationMapper(Mapper):
    _ENTITY = RealTimeLocation
    _MODEL = 

    @staticmethod
    def _build_map(record):
    	return {};

    @staticmethod
    def _to_record(entity):
        params = {
            'token': entity.token,
            'latitude': entity.vehicle_location.latitude,
            'longitude': entity.vehicle_location.longitude,
        }
        if entity.level:
            params.update({'level': entity.level})
        if entity.description:
            params.update({'description': entity.description})
        
        return params

    @classmethod
    def _to_model(cls, entity):
        return cls._MODEL(**{})