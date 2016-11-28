from datetime import datetime
from schematics.types import (
    StringType,
    FloatType,
    IntType,
    DateTimeType,
)
from schematics.types.compound import ModelType
from ParkingFinder.entities.entity import Entity
from ParkingFinder.entities.location import Location


class ParkingSpace(Entity):
    """
    Parking Space Entity
    
    """
    # required variables
    plate = StringType(min_length=7, max_length=7, required=True)
    location = ModelType(model_class=Location, required=True)
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f', default=datetime.utcnow)

    @classmethod
    def get_mock_object(cls, context=None, overrides=None):
        obj = super(ParkingSpace, cls).get_mock_object(context=context, overrides=overrides)
        location = overrides and overrides.get('location', None)
        if location:
            obj.location = location
        else:
            obj.location = Location.get_mock_object()
        return obj
