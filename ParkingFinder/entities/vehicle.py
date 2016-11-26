from schematics.types import (
    StringType,
    IntType,
)
from ParkingFinder.entities.entity import Entity


class Vehicle(Entity):
    """
    Vehicle Entity
    """
    # required variables
    plate = StringType(min_length=1, max_length=7, required=True)
    brand = StringType(min_length=1, max_length=32, required=True)
    model = StringType(min_length=1, max_length=32, required=True)
    color = StringType(min_length=1, max_length=32, required=True)
    year = IntType(min_value=1900, max_value=2017, required=True)
