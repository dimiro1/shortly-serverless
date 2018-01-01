"""Collection of AWS service implementations"""

import time
import os
import base62
import random


class Database:
    """Database mock"""

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.urls = dynamodb.Table(os.environ['DYNAMODB_URLS_TABLE'])

    def insert(self, _id, data):
        """Insert into dictionary"""
        timestamp = int(time.time() * 1000)
        item = {
            'id': _id,
            'long_url': data['long_url'],
            'created_at': timestamp,
            'updated_at': timestamp,
        }
        self.urls.put_item(Item=item)

    def get(self, _id):
        """Get from dictionary"""

        item = self.urls.get_item(
            Key={
                'id': _id
            }
        )
        return item


class AtomicCounter:
    """Atomic counter mock"""

    def __init__(self):
        pass

    def next(self):
        return random.randint(0, 999999999)
