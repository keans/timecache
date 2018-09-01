import datetime
import threading
import logging

from .cachentry import CacheEntry
from .backends.memorybackend import MemoryBackend
from .consts import DEFAULT_DURATION


# setup custom logger
log = logging.getLogger(__name__)

# default backend of a cache
DEFAULT_BACKEND = MemoryBackend()


class Cache:
    """
    simple timeout-based cache to store key, value pairs
    using different storing backends
    """
    def __init__(
            self, backend=DEFAULT_BACKEND, default_duration=DEFAULT_DURATION,
            auto_load=True
    ):
        self._d = {}

        self.backend = backend
        self._default_duration = default_duration
        self.__lock = threading.RLock()

        if (auto_load is True) and (self.backend.is_existing):
            # auto load stored data
            self.load()

    @property
    def is_persistent(self):
        """
        returns True, when backend supports persistence
        """
        return self.backend.is_persistent

    @property
    def is_existing(self):
        """
        returns True, when backend is existing
        """
        return self.backend.is_existing

    @property
    def filename(self):
        """
        returns the backend of the filename if persistent, else None
        """
        if self.is_persistent is True:
            return self.backend.filename

        return None

    def _remove_expired(self):
        """
        remove all expired items in a lazy fashion
        (will be called by all functions that read the cache)
        """
        with self.__lock:
            is_changed = False
            for k in list(self._d.keys()):
                if self._d[k].is_expired():
                    log.debug("removing expired item: {}".format(self._d[k]))
                    del self[k]
                    is_changed = True

        if (is_changed is True) and (self.is_persistent):
            # save changed cache file
            self.save()

    def __setitem__(self, key, item):
        """
        set item by key via [] operator
        """
        with self.__lock:
            cache_entry = CacheEntry(item, DEFAULT_DURATION)
            log.debug("__setitem__: {}".format(cache_entry))
            self._d[key] = cache_entry

    def __getitem__(self, key):
        """
        get item by key via [] operator;
        """
        self._remove_expired()

        cache_entry = self._d.get(key, None)
        log.debug("__getitem__: {}".format(cache_entry))

        return cache_entry

    def __contains__(self, key):
        """
        returns True, if key in items
        """
        self._remove_expired()

        log.debug("__contains__: {}".format(key))
        return key in self._d

    def __delitem__(self, key):
        """
        delete item by key
        """
        with self.__lock:
            log.debug("__delitem__: {}".format(key))
            del self._d[key]

    def __len__(self):
        """
        return length
        """
        self._remove_expired()

        return len(self._d)

    def __repr__(self):
        """
        return printable representation of the cache
        """
        return "<Cache(backend={}, cached_items={}, len_items={})".format(
            self.backend, list(self.items()), len(self)
        )

    def keys(self):
        """
        return all valid keys of the cache
        """
        self._remove_expired()

        return self._d.keys()

    def values(self):
        """
        return all valid values of the cache
        """
        self._remove_expired()

        return self._d.values()

    def items(self):
        """
        return all items of the cache
        """
        self._remove_expired()

        return self._d.items()

    def get(self, key):
        """
        return item by key of the cache
        """
        return self[key]

    def set(self, key, item, duration=DEFAULT_DURATION):
        """
        set an item to the given key and set duration
        """
        assert isinstance(duration, datetime.timedelta)

        with self.__lock:
            self._d[key] = CacheEntry(item, duration)

    def remove(self, key):
        """
        remove item by key of the cache
        """
        del self[key]

    def load(self):
        """
        load cached data via the backend
        """
        with self.__lock:
            log.debug("load: {}".format(self.backend.filename))
            self._d.update(self.backend.load())

    def save(self):
        """
        save cached data via the backend
        """
        log.debug("save: {}".format(self.backend.filename))
        self.backend.save(list(self._d.items()))
