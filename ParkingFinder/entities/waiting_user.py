from schematics.types import (
    StringType,
    FloatType,
    IntType,
    DateTimeType,
    BooleanType,
)
from schematics.types.compound import ModelType

from ParkingFinder.entities.entity import Entity
from ParkingFinder.entities.location import Location


class WaitingUser(Entity):
    """
    Waiting User Entity

    """
    # required variables
    user_id = StringType(min_length=1, max_length=64, required=True)
    location = ModelType(model_class=Location, required=True)
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')
    is_active = BooleanType(required=True, default=False)

    @classmethod
    def get_mock_object(cls, context=None, overrides=None):
        obj = super(WaitingUser, cls).get_mock_object(context=context, overrides=overrides)
        location = overrides and overrides.get('location', None)
        if location:
            obj.location = location
        else:
            obj.location = Location.get_mock_object()
        return obj

