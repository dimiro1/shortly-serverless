"""Collection of mock implementations for the shortly service"""


class Database:
    """Database mock"""

    def __init__(self):
        self.urls = {}

    def insert(self, _id, data):
        """Insert into dictionary"""
        self.urls[_id] = data

    def get(self, _id):
        """Get from dictionary"""
        return self.urls[_id]


class Notifier:
    """Notifier Mock"""

    def __init__(self):
        pass

    def notify(self, _id):
        """Just print in stdout"""
        print('Created {}'.format(_id))


class AtomicCounter:
    """Atomic counter mock"""

    def __init__(self):
        self.current = 0

    def next(self):
        """Increment and return the next integer in the sequence"""
        self.current += 1
        return self.current
