# -*- coding: utf-8 -*-

from tornado.gen import coroutine


class RealTimeLocationService(object):

    @classmethod
    @coroutine
    def fetch_real_time_location(cls, token):
        """
        Fetch the real time location entity by token

        :return:
        """
        pass
