"""Default hasher implementation"""

import base62


class Hasher:
    """Hasher"""

    def hash(self, an_int):
        """Hash with base62"""
        return base62.encode(an_int)
