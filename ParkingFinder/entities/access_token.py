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

    @property
    def is_expired(self):
        delta = datetime.utcnow() - self.expires_at
        return delta.total_seconds() >= 0
