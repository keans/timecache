from .basebackend import BaseBackend, NotPersistentException


class MemoryBackend(BaseBackend):
    """
    memory backend that is the simplest form of backend
    that supports no persistence
    """
    @property
    def is_persistent(self):
        """
        return persistent state
        """
        return False

    @property
    def is_existing(self):
        """
        return True, when backend is existing
        """
        return False

    def load(self):
        """
        since in memory it is not possible to load the cached data
        """
        raise NotPersistentException

    def save(self, data):
        """
        since in memory it is not possible to save the cached data
        """
        raise NotPersistentException
