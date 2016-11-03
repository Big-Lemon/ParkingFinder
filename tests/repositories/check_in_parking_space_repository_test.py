import pytest

from doubles import expect
from schematics.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.repositories import check_in_parking_space_repository as module
