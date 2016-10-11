from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
)

from ParkingFinder.tables.base import Base


class AccessToken(Base):
    __tablename__ = 'access_tokens'

    access_token = Column(String(255), primary_key=True)
    user_id = Column(String(64), ForeignKey('users.user_id'), index=True)
    expires_at = Column(DateTime, nullable=False)
    issued_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return 'access_token: {}, ' \
               'user_id: {}, ' \
               'expires_at: {}, ' \
               'issued_at: {}'.format(
                self.access_token,
                self.user_id,
                str(self.expires_at),
                str(self.issued_at),
        )
