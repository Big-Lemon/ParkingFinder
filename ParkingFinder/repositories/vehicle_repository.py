from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.async_db import create_session
from ParkingFinder.base.errors import NotFound
from ParkingFinder.mappers.vehicle_mapper import VehicleMapper
from ParkingFinder.tables.vehicle import Vehicles
from ParkingFinder.tables.registered_vehicles import RegisteredVehicles


class VehicleRepository(object):

    @staticmethod
    @coroutine
    def retrieve_vehicle_by_plate(plate):
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

    @classmethod
    @coroutine
    def retrieve_vehicle_by_user(cls, user_id):
        """
        Retrieve a vehicle by user id
        :param str user_id:
        :return list[Vehicle]:
        """
        with create_session() as session:
            vehicles = session.query(RegisteredVehicles).filter(RegisteredVehicles.user_id == user_id).all()
            entities = []
            for vehicle in vehicles:
                _vehicle = yield cls.retrieve_vehicle_by_plate(plate=vehicle.plate)
                entities.append(_vehicle)
            raise Return(entities)

    @classmethod
    @coroutine
    def insert_registered_vehicle(cls, user_id, vehicle):
        """
        Add a new vehicle to an existing user

        :param str user_id: owner of the vehicle
        :param Vehicle vehicle:
        :return Vehicle vehicle: inserted vehicle
        """

        with create_session() as session:
            _vehicle = yield cls._insert_vehicle(vehicle)
            registered_vehicle_model = RegisteredVehicles(user_id=user_id, plate=vehicle.plate)
            session.add(registered_vehicle_model)
            raise Return(_vehicle)

    @classmethod
    @coroutine
    def delete_registered_vehicle(cls, user_id, vehicle):
        """
        Delete a relationship between an user and his car, then delete his car from db
        :param str user_id:
        :param Vehicle vehicle:
        :return Vehicle vehicle: deleted vehicle
        """

        with create_session() as session:
            session.query(RegisteredVehicles).filter(RegisteredVehicles.user_id == user_id).delete()
            _vehicle = yield cls._delete_vehicle(vehicle=vehicle)
            raise Return(_vehicle)

    @staticmethod
    @coroutine
    def _insert_vehicle(vehicle):
        """
        Insert a vehicle into db

        :param Vehicle vehicle:
        :return Vehicle vehicle: inserted vehicle
        """
        with create_session() as session:
            vehicle.validate()
            _vehicle = VehicleMapper.to_model(vehicle)
            session.add(_vehicle)
            raise Return(vehicle)

    @staticmethod
    @coroutine
    def _delete_vehicle(vehicle):
        """
        Delete a vehicle in db

        :param Vehicle vehicle:
        :return Vehicle vehicle: deleted vehicle
        """
        with create_session() as session:
            vehicle.validate()
            # _vehicle = VehicleMapper.to_model(vehicle)
            # session.delete(_vehicle)
            session.query(Vehicles).filter(Vehicles.plate == vehicle.plate).delete()
            raise Return(vehicle)


class VehicleNotFound(NotFound):
    error = 'Vehicle Not Found'
