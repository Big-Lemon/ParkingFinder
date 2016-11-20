from abc import ABCMeta, abstractmethod

from ParkingFinder.base.errors import InvalidArguments


class Mapper:
    """
    Base Abstract Mapper function
    This Mapper provides three methods:
        to_entity   Model => Entity
        to_model    Entity => Model
        to_record   Entity => Json

    This mapper requires to implement corresponding abstract methods.
        to_entity    requires   _to_entity
        to_model     requires   _to_model
        to_record    requires   _to_record
    Those abstract method provides custom mapping Functionality

    The Subclass is required to assign a class to _ENTITY and _MODEL,
    and only the objects with same type as _ENTITY/_MODEL are supported
    with the mapper

    """
    __metaclass__ = ABCMeta
    _ENTITY = None
    _MODEL = None

    def __init__(self):
        if not self._ENTITY:
            raise NotImplementedError

    @classmethod
    def to_entity(cls, record, *args, **params):
        """
        Map from sqlalchemy model to schematics entity
        This function will use _build_map to generate a json object that
        is required to create the entity

        :param Model record: sqlalchemy model
        :return Entity: schematics enttity
        :raises NotImplementedError: the mapper is called without
                implementing abstract method `_build_map()`
        """
        params = cls._build_map(record, *args, **params)
        return cls._ENTITY(params)

    @staticmethod
    @abstractmethod
    def _build_map(record, *args, **params):
        """
        Abstract method that is required to be implemented before using to_entity

        :param Model record:
        :return json:
        """
        raise NotImplementedError

    @classmethod
    def to_record(cls, entity):
        """
        Map from schematics entity to json object

        This method will use `_to_record` to generate the parameters
        that are required by corresponding entity


        :param Entity entity: schematics
        :return json: primitive object
        :raises InvalidArguments: The mapper doesn't support entity passed in
        """
        if not isinstance(entity, cls._ENTITY):
            raise InvalidArguments
        return cls._to_record(entity)

    @staticmethod
    @abstractmethod
    def _to_record(entity):
        """
        Abstract method that is required to be implemented before using to_record

        :param entity:
        :return json: primitive entity
        :raises NotImplementedError:
        """
        raise NotImplementedError

    @classmethod
    def to_model(cls, entity):
        """
        Map from schematics entity to sqlalchemy model

        This function will use `_to_model` method to generate the parameters
        that are required by corresponding model

        :param Entity entity: schematics entity
        :return Model: sqlalchemy model
        """
        if not isinstance(entity, cls._ENTITY):
            raise InvalidArguments
        if not cls._MODEL:
            raise NotImplementedError
        return cls._to_model(entity)

    @staticmethod
    @abstractmethod
    def _to_model(cls, entity):
        """
        Abstract method that is required to be implemented before using to_model
        :param cls:
        :param Entity entity:
        :return **json:
        """
        raise NotImplementedError
