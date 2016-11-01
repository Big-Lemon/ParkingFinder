import httplib
import json
from datetime import datetime

from clay import config
from sqlalchemy.orm.exc import NoResultFound
from tornado.auth import FacebookGraphMixin
from tornado.gen import coroutine

from ParkingFinder.base.errors import NotFound
from ParkingFinder.entities.access_token import AccessToken
from ParkingFinder.entities.user import User
from ParkingFinder.handlers.handler import BaseHandler
from ParkingFinder.mappers.access_token_mapper import AccessTokenMapper
from ParkingFinder.mappers.user_mapper import UserMapper
from ParkingFinder.repositories.access_token_repository import AccessTokenRepository
from ParkingFinder.services.user import UserService

logger = config.get_logger('handler.auth.login')


class FacebookGraphLoginHandler(BaseHandler, FacebookGraphMixin):

    @coroutine
    def get(self):
        # TODO this handler function should split into service and facebook gateway in lower level
        access_token = self.get_argument("access_token", False)
        if not access_token:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': 'Access Token Required',
            })

        else:
            try:
                response = yield self.facebook_request(
                    "/debug_token?input_token={}&access_token={}|{}".format(
                        access_token,
                        config.get("oauth2.facebook.app_id"),
                        config.get("oauth2.facebook.app_secret"),
                    ))
                if not response:
                    self.set_status(httplib.BAD_GATEWAY)
                    self.write({
                        'error': 'Can Not Inspect Access Token',
                    })

                data = response['data']
                logger.info({
                    'message': 'Inspect Access Token',
                    'data': data
                })
                if data['is_valid']:
                    try:
                        # check if user exist
                        user = yield UserService.get_user_detail(
                            user_id=data['user_id']
                        )
                    except NotFound:
                        # first time login, retrieve public profile
                        fields = [
                            'id',
                            'first_name',
                            'last_name',
                            'email',
                            'picture'
                        ]
                        fb_user = yield self.facebook_request(
                            "/me?fields={}&access_token={}".format(
                                ','.join(fields),
                                access_token,
                            )
                        )
                        logger.info({
                            'message': 'Retrieve user public profile',
                            'fb_user': fb_user
                        })
                        # add a new user into db
                        user = yield UserService.register(
                            User({
                                'user_id': fb_user['id'],
                                'first_name': fb_user['first_name'],
                                'last_name': fb_user['last_name'],
                                'profile_picture_url': fb_user.get('picture').get('data').get('url'),
                            })
                        )

                    access_token = AccessToken({
                        'user_id': data['user_id'],
                        'expires_at': datetime.fromtimestamp(data.get('expires_at')),
                        'issued_at': datetime.fromtimestamp(data.get('issued_at')),
                        'access_token': access_token
                    })

                    token = yield UserService.update_access_token(
                        access_token=access_token
                    )

                    user_res = UserMapper.to_record(user)
                    token_res = AccessTokenMapper.to_record(token)

                    self.set_status(httplib.OK)
                    self.write({
                        'user': user_res,
                        'access_token': token_res
                    })
                else:
                    logger.warn({
                        'message': 'Invalid Token ',
                        'data': data
                    })

                    self.set_status(httplib.UNAUTHORIZED)
                    self.write({
                        'error': 'Invalid Access Token',
                        'payload': {
                            'access_token': access_token
                        }
                    })
            except Exception as ex:
                logger.error({
                    'error': 'UnexpectedError',
                    'data': ex
                })
                self.set_status(httplib.BAD_GATEWAY)
                self.write({
                    'error': 'Facebook Gateway Error'
                })

    @coroutine
    def post(self):
        payload = json.loads(self.request.body)
        access_token = self.get_argument("access_token", False)

        if not access_token:
            access_token = payload.get('access_token', False)

        if not access_token:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': 'Access Token Required',
            })
        try:
            yield AccessTokenRepository.remove(
                access_token=access_token
            )
            self.set_status(httplib.OK)
        except NoResultFound:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': 'Not Found',
                'payload': {
                    'access_token': access_token
                }
            })
