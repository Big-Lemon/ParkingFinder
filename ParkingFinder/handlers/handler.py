from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    """
    Base Handler class
    """

    @property
    def url(self):
        return (
            "%s://%s%s" %
            (self.request.protocol,
             self.request.host,
             self.request.uri
             )
        )

    def read_one(self, *args, **params):
        """
        Read one entity from database

        :param args:
        :param params:
        :return:
        """
        pass

    def read_many(self, *args, **params):
        """
        Read many entities from database


        :param args:
        :param params:
        :return:
        """
        pass

    def update(self, *args, **params):
        """
        Update the entity

        :param args:
        :param params:
        :return:
        """

    def upsert(self, *args, **params):
        """
        Update entity if exist, insert a new one into database

        :param args:
        :param params:
        :return:
        """

    def remove(self, *args, **params):
        """
        Remove an entity from database

        :param args:
        :param params:
        :return:
        """

    def insert(self, *args, **params):
        """
        Insert a new Entity into DB

        :param args:
        :param params:
        :return:
        """
