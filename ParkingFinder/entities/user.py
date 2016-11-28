from schematics.types import (
    StringType,
    URLType,
)
from schematics.types.compound import ListType, ModelType

from ParkingFinder.entities.entity import Entity
from ParkingFinder.entities.vehicle import Vehicle


class User(Entity):
    """
    User Entity
    """
    # required variables
    user_id = StringType(min_length=1, max_length=64, required=True)
    first_name = StringType(min_length=1, max_length=32, required=True)
    last_name = StringType(min_length=1, max_length=32, required=True)

    # non-required variables
    profile_picture_url = URLType(max_length=255, required=False)
    activated_vehicle = StringType(min_length=1, max_length=7, required=False)
    owned_vehicles = ListType(ModelType(Vehicle))

