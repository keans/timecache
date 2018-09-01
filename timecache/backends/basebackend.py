from abc import ABCMeta, abstractmethod, abstractproperty


class NotPersistentException(Exception):
    """
    exception that is thrown when a cache backend should store/load
    persistent data, but is not a persistent storage
    """
    pass


class BaseBackend:
    """
    abstract class that should be implemented by all
    cache storage backends
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def is_persistent(self):
        """
        return True, when backend is storing the data persistently
        """
        return NotImplemented

    @abstractproperty
    def is_existing(self):
        """
        return True, when backend is existing
        """
        return NotImplemented

    @abstractmethod
    def load(self):
        """
        load persistent cache data
        """
        return NotImplemented

    @abstractmethod
    def save(self, data):
        """
        save persistent cache data
        """
        return NotImplemented

    def __str__(self):
        """
        human readable string output
        """
        return "<{}>".format(self.__class__.__name__)
