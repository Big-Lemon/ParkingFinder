from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.async_db import create_session
from ParkingFinder.base.errors import NotFound
from ParkingFinder.mappers.vehicle_mapper import  import VehicleMapper
from ParkingFinder.tables.vehicle import Vehicles


class VehicleRepository(object):

    @staticmethod
    @coroutine
    def retrieve_car_by_plate(plate):
        """
        Retrieve a vehicle by plate

        :param str plate:
        :return Vehicle:
        :raises sqlalchemy.orm.exc.NoResultFound:
        """
        with create_session() as session:
            vehicle = session.query(Vehicles).filter(
                Vehicles.plate == plate
            ).one()
            entity = VehicleMapper.to_entity(record=vehicle)
            raise Return(entity)


    #TODO: insert, update, upsert