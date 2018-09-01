import datetime

from .consts import DEFAULT_DURATION, FOREVER


class CacheEntry:
    """
    the cache consists of one or multiple CacheEntry object,
    each have a creation time, a duration and a set value.
    """
    def __init__(self, value, duration=DEFAULT_DURATION):
        self.creation_time = datetime.datetime.now()
        self.duration = duration
        self.value = value

    @property
    def expiration_time(self):
        """
        datetime when the cache entry expires
        """
        if self.duration is FOREVER:
            return None

        return self.creation_time + self.duration

    def is_expired(self):
        """
        returns True, if cache entry is expired
        """
        if self.duration is FOREVER:
            return False

        return self.expiration_time < datetime.datetime.now()

    def __repr__(self):
        return (
            "<CacheEntry(creation_time={}, duration={}, "
            "expiration_time={}, is_expired={}, value={})>".format(
                self.creation_time, self.duration,
                self.expiration_time or "never",
                self.is_expired(),
                repr(self.value)
            )
        )
