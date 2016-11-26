from tornado.gen import coroutine, Return
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.base.async_db import create_session
from ParkingFinder.mappers.parking_space_mapper import ParkingSpaceMapper
from ParkingFinder.tables.parking_lot import ParkingLot


from ParkingFinder.base.async_db import create_session
from ParkingFinder.base.errors import NotFound
from ParkingFinder.mappers.parking_space_mapper import ParkingSpaceMapper
from ParkingFinder.tables.parking_lot import ParkingLot

class ParkingLotRepository(object):

    @classmethod
    @coroutine
    def read_one(cls, plate):
        """
        Read one by plate

        :param str plate:
        :return: <ParkingSpace>:
        :raises noResultFound: vehicle with given plate is not in the parking lot
        """
        with create_session() as session:
            parkinglot = session.query(ParkingLot).filter(
                ParkingLot.plate == plate
            ).one()
            entity = ParkingSpaceMapper.to_entity(record=parkinglot)

            raise Return(entity)


    @classmethod
    @coroutine
    def insert(cls, parking_space):
        """
        Insert a parking space to the parking lot

        :return ParkingSpace:
        """
        with create_session() as session:
            parking_space.validate()
            _parking_space = ParkingSpaceMapper.to_model(parking_space)
            session.add(_parking_space)
            raise Return(parking_space)

    @classmethod
    @coroutine
    def upsert(cls, parking_space):
        """
        Insert a parking space to the parking lot

        :return ParkingSpace:
        """
        with create_session() as session:
            try:
                _parking_space = session.query(ParkingLot).filter(
                    ParkingLot.plate == parking_space.plate
                ).one()
                _parking_space.latitude = str(parking_space.location.latitude)
                _parking_space.longitude = str(parking_space.location.longitude)
                raise Return(parking_space)
            except NoResultFound:
                parking_space.validate()
                _parking_space = ParkingSpaceMapper.to_model(parking_space)
                session.add(_parking_space)
                raise Return(parking_space)

    @classmethod
    @coroutine
    def remove(cls, plate):
        """
        Remove a parking space by the plate from parking lot

        :return:
        """
        with create_session() as session:
            row = session.query(ParkingLot).filter(
                ParkingLot.plate == plate
            ).delete()
            if row == 0:
                raise NoResultFound
            raise Return(row)

