from ParkingFinder.entities.entity import Entity
from ParkingFinder.mappers import Mapper
from ParkingFinder.entities.matched_parking_space import MatchedParkingSpace
from ParkingFinder.tables.matched_parking_space_list import MatchedParkingSpaceList

class MatchedParkingSpaceMapper(Mapper):
    _ENTITY = MatchedParkingSpace
    _MODEL = MatchedParkingSpaceList

    @staticmethod
    def _build_map(record):
        return {
            'user_id': record.user_id,
            'plate': record.plate,
            'status': record.status,
            'created_at': record.created_at,
        }

    @staticmethod
    def _to_record(entity):
        return entity.to_primitive()

    @classmethod
    def _to_model(cls, entity):
        return cls._MODEL(**{
            'user_id': entity.user_id,
            'plate': entity.plate,
            'status': entity.status,
            'created_at': entity.created_at,
        })
