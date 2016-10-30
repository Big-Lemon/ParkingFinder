from ParkingFinder.tables.vehicle import Vehicles
from ParkingFinder.entities.vehicle import Vehicle
from ParkingFinder.mappers import Mapper

class VehicleMapper(Mapper):
    _ENTITY = Vehicle
    _MODEL = Vehicles

    @staticmethod
    def _build_map(record):
        params = {
            'plate': record.plate,
            'brand': record.brand,
            'model': record.model,
            'color': record.color,
            'year': record.year,
        }
        return params


    @staticmethod
    def _to_record(entity):
        params = entity.to_primitive()

        return params


    @classmethod
    def _to_model(cls, entity):
        params = entity.to_primitive()

        return cls._MODEL(**params)
