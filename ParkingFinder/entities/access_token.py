from datetime import datetime

from schematics.types import (
    StringType,
    DateTimeType,
)
from ParkingFinder.entities.entity import Entity


class AccessToken(Entity):
    """
    Access Token
    """
    user_id = StringType(required=True)
    access_token = StringType(required=True)
    issued_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')
    expires_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')

    @classmethod
    def is_expired(cls):
        delta = datetime.utcnow() - cls.expires_at
        return delta.total_seconds() >= 0
