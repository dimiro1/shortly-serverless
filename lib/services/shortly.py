"""This file contains the shortly service implementation"""

import re
import logging

LOGGER = logging.getLogger()


class NotFound(Exception):
    """URL could not be found"""
    pass


class InternalError(Exception):
    """An unexpected error"""
    pass


class Shortly:
    """Shortly is the abstraction for the shortly service"""

    def __init__(self, hasher, integer_pool, database, notifier):
        self.hasher = hasher
        self.integer_pool = integer_pool
        self.database = database
        self.notifier = notifier

    def info(self, _id):
        """Collect and return information data about the given id"""

        try:
            return self.database.get(_id)
        except Exception as e:
            LOGGER.error('Request an URL that does not exists %s', e)
            raise NotFound()

    def create(self, long_url):
        """Create a new short url"""

        number = self.integer_pool.next()
        _id = self.hasher.hash(number)

        to_insert = {
            'long_url': long_url,
            'id': _id,
        }

        try:
            self.database.insert(_id, to_insert)
        except:
            LOGGER.error('An internal error just happened')
            raise InternalError()

        self.notifier.notify(_id)

        return to_insert
