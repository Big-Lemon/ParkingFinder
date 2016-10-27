import httplib
import time
from datetime import datetime

from clay import config
from tornado.auth import FacebookGraphMixin
from tornado.gen import coroutine

from ParkingFinder.base.errors import NotFound
from ParkingFinder.entities.access_token import AccessToken
from ParkingFinder.entities.user import User
from ParkingFinder.handlers.handler import BaseHandler
from ParkingFinder.mappers.access_token_mapper import AccessTokenMapper
from ParkingFinder.mappers.user_mapper import UserMapper
from ParkingFinder.services.user import UserService

logger = config.get_logger('handler.auth.login')


class FacebookGraphLoginHandler(BaseHandler, FacebookGraphMixin):

    @coroutine
    def get(self):
        if self.get_argument("code", False):

            # short term access
            fb_user = yield self.get_authenticated_user(
                redirect_uri=self.url,
                client_id=config.get("oauth2.facebook.app_id"),
                client_secret=config.get("oauth2.facebook.app_secret"),
                code=self.get_argument("code"),
            )
            # long-term access token: 60 days.
            logger.info({'user_id': fb_user['id'], 'access_token': fb_user['access_token']})

            try:
                # check if user exist
                user = yield UserService.get_user_detail(
                    user_id=fb_user['id']
                )
                # if user not exist, login method will throw NotFound exception
            except NotFound:
                # add a new user into db
                user = yield UserService.register(
                    User({
                        'user_id': fb_user['id'],
                        'first_name': fb_user['first_name'],
                        'last_name': fb_user['last_name'],
                        'profile_picture_url': fb_user.get('picture').get('data').get('url'),
                    })
                )

            now = time.time()
            access_token = AccessToken({
                'user_id': fb_user['id'],
                'expires_at': datetime.fromtimestamp(now + int(fb_user.get('session_expires')[0])),
                'issued_at': datetime.fromtimestamp(now),
                'access_token': fb_user['access_token']
            })

            token = yield UserService.update_access_token(
                access_token=access_token
            )

            user_res = UserMapper.to_record(user)
            token_res = AccessTokenMapper.to_record(token)

            self.set_status(httplib.OK)
            self.write({
                'user': user_res,
                'token': token_res
            })
        else:
            yield self.authorize_redirect(
                redirect_uri=self.url,
                client_id=config.get("oauth2.facebook.app_id"),
                extra_params={"scope": "public_profile"})
