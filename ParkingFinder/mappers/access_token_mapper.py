from datetime import datetime

from ParkingFinder.mappers import Mapper
from ParkingFinder.entities.access_token import AccessToken


class AccessTokenMapper(Mapper):
    _ENTITY = AccessToken

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
            'issued_at': entity.issued_at,
            'expires_at': entity.expires_at,
        }
