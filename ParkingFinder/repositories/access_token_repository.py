from tornado.gen import coroutine, Return
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.base.async_db import with_session
from ParkingFinder.mappers.access_token_mapper import AccessTokenMapper
from ParkingFinder.tables.access_token import AccessToken


class AccessTokenRepository(object):

    @staticmethod
    @with_session
    def read_one(access_token, session):
        """

        :param access_token:
        :param Session session:
        :return:
        :raises NoResultFound:
        """
        access_token = session.query(AccessToken).filter(
            AccessToken.access_token == access_token
        ).one()
        entity = AccessTokenMapper.to_entity(record=access_token)
        raise Return(entity)

    @staticmethod
    @with_session
    def read_many(user_id, session):
        """

        :param user_id:
        :param session:
        :return:
        """
        access_tokens = session.query(AccessToken).filter(
            AccessToken.user_id == user_id
        ).all()
        entities = [
            AccessTokenMapper.to_entity(record=access_token)
            for access_token in access_tokens
            ]

        raise Return(entities)

    @classmethod
    @with_session
    def upsert(cls, access_token, expires_at, session, user_id=None, issued_at=None):
        """
        Update 'expires_at' if access_token is already existed in database,
        otherwise create a new access token and insert into db.

        :param str access_token:
        :param datetime.datetime expires_at:
        :param Session session:
        :param str user_id:
        :param datetime.datetime issued_at:
        :return:
        :raises:
        """
        try:
            token = session.query(AccessToken).filter(
                AccessToken.access_token == access_token
            ).one()
            token.expires_at = expires_at
            entity = AccessTokenMapper.to_entity(record=token)
            raise Return(entity)
        except NoResultFound:
            _token = AccessToken(
                access_token=access_token,
                expires_at=expires_at,
                user_id=user_id,
                issued_at=issued_at,
            )
            session.add(_token)
            entity = AccessTokenMapper.to_entity(record=_token)
            raise Return(entity)

    @staticmethod
    @with_session
    def remove(access_token, session):
        """
        remove a access_token if exist

        :param str access_token:
        :param Session session:
        :return:
        """
        rows = session.query(AccessToken).filter(
            AccessToken.access_token == access_token
        ).delete()
        if rows == 0:
            raise NoResultFound

        raise Return(rows)
