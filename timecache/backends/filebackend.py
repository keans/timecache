import os

from .basebackend import BaseBackend


class FileBackend(BaseBackend):
    """
    simple file backend that is the simplest form of backend
    that supports persistence
    """

    @property
    def is_persistent(self):
        """
        return persistent state
        """
        return True

    @property
    def is_existing(self):
        """
        return True, when backend is existing
        """
        return os.path.exists(self.filename)

    def load(self):
        """
        override this with a custom implementation
        """
        raise NotImplemented

    def save(self, data):
        """
        override this with a custom implementation
        """
        raise NotImplemented

    def __str__(self):
        """
        human readable string output
        """
        return "<{}(filename='{}')>".format(
            self.__class__.__name__, self.filename,
        )

