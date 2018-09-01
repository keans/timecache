import os
import pickle

from .filebackend import FileBackend


class PickleBackend(FileBackend):
    """
    backend to store and load cached data from pickle file
    """
    def __init__(self, filename=None):
        FileBackend.__init__(self)
        self.filename = filename or "cache.pickle"

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
        load cached data from pickle file
        """
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                return pickle.load(f)

        return None

    def save(self, data):
        """
        save cached data to pickle file
        """
        with open(self.filename, "wb") as f:
            pickle.dump(data, f)
