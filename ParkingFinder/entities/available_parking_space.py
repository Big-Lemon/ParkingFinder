from datetime import datetime

from schematics.types import (
    BooleanType,
    DateTimeType,
    StringType,
    IntType,
)
from schematics.types.compound import ModelType

from ParkingFinder.entities.entity import Entity
from ParkingFinder.entities.location import Location


class AvailableParkingSpace(Entity):
    """
    Parking Space Entity with posting status

    """
    # required variables

    plate = StringType(min_length=7, max_length=7, required=True)
    location = ModelType(model_class=Location, required=True)
    is_active = BooleanType(required=True, default=False)
    expired_at = DateTimeType(
        required=True,
        formats='%Y-%m-%d %H:%M:%S.%f',
        serialized_format='%Y-%m-%d %H:%M:%S.%f',
        default=datetime.utcnow
    )
    distance = IntType(required=False)

    @classmethod
    def get_mock_object(cls, context=None, overrides=None):
        obj = super(AvailableParkingSpace, cls).get_mock_object(context=context, overrides=overrides)
        location = overrides and overrides.get('location', None)
        if location:
            obj.location = location
        else:
            obj.location = Location.get_mock_object()
        return obj

