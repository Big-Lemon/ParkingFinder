from tornado.gen import coroutine, Return
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.base.async_db import create_session
from ParkingFinder.mappers.access_token_mapper import AccessTokenMapper
from ParkingFinder.tables.access_token import AccessToken


class AccessTokenRepository(object):

    @staticmethod
    @coroutine
    def read_one(access_token):
        """

        :param access_token:
        :return:
        :raises NoResultFound:
        """
        with create_session() as session:
            access_token = session.query(AccessToken).filter(
                AccessToken.access_token == access_token
            ).one()
            entity = AccessTokenMapper.to_entity(record=access_token)
            raise Return(entity)

    @staticmethod
    @coroutine
    def read_many(user_id):
        with create_session() as session:
            access_tokens = session.query(AccessToken).filter(
                AccessToken.user_id == user_id
            ).all()
            entities = [
                AccessTokenMapper.to_entity(record=access_token)
                for access_token in access_tokens
                ]

            raise Return(entities)

    @classmethod
    @coroutine
    def upsert(cls, access_token, expires_at, user_id=None, issued_at=None):
        """
        Update 'expires_at' if access_token is already existed in database,
        otherwise create a new access token and insert into db.

        :param str access_token:
        :param datetime.datetime expires_at:
        :param str user_id:
        :param datetime.datetime issued_at:
        :return:
        :raises:
        """
        with create_session() as session:
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
    @coroutine
    def remove(access_token):
        """
        remove a access_token if exist

        :param str access_token:
        :return:
        """
        with create_session() as session:
            rows = session.query(AccessToken).filter(
                AccessToken.access_token == access_token
            ).delete()
            if rows == 0:
                raise NoResultFound

            raise Return(rows)
