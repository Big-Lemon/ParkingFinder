from datetime import datetime

from ParkingFinder.mappers import Mapper
from ParkingFinder.entities.access_token import AccessToken
from ParkingFinder.tables.access_token import AccessToken as AccessTokenModel


class AccessTokenMapper(Mapper):
    _ENTITY = AccessToken
    _MODEL = AccessTokenModel

    @staticmethod
    def _build_map(record):
        return {
            'user_id': record.user_id,
            'access_token': record.access_token,
            'issued_at': record.issued_at,
            'expires_at': record.expires_at
        }

    @staticmethod
    def _to_record(entity):
        return {
            'user_id': entity.user_id,
            'access_token': entity.access_token,
            'issued_at': str(entity.issued_at),
            'expires_at': str(entity.expires_at),
        }

    @classmethod
    def _to_model(cls, entity):
        return cls._MODEL(**{
            'user_id': entity.user_id,
            'access_token': entity.access_token,
            'issued_at': entity.issued_at,
            'expires_at': entity.expires_at,
        })
