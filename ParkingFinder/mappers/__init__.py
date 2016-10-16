from abc import ABCMeta, abstractmethod

from ParkingFinder.base.errors import InvalidArguments


class Mapper:
    __metaclass__ = ABCMeta
    _ENTITY = None
    _MODEL = None

    def __init__(self):
        if not self._ENTITY:
            raise NotImplementedError

    @classmethod
    def to_entity(cls, record):
        params = cls._build_map(record)
        return cls._ENTITY(params)

    @staticmethod
    @abstractmethod
    def _build_map(record):
        raise NotImplementedError

    @classmethod
    def to_record(cls, entity):
        if not isinstance(entity, cls._ENTITY):
            raise InvalidArguments
        return cls._to_record(entity)

    @staticmethod
    @abstractmethod
    def _to_record(entity):
        raise NotImplementedError

    @classmethod
    def to_model(cls, entity):
        if not isinstance(entity, cls._ENTITY):
            raise InvalidArguments
        if not cls._MODEL:
            raise NotImplementedError
        return cls._to_model(entity)

    @staticmethod
    @abstractmethod
    def _to_model(cls, entity):
        raise NotImplementedError
