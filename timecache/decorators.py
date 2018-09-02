import hashlib
from functools import wraps, partial

from .consts import DEFAULT_DURATION
from .timecache import Cache, log
from .backends import MemoryBackend, JsonBackend, PickleBackend


def cache(backend, cache_filename="", ttl=DEFAULT_DURATION):
    """
    basic cache decorator
    """
    cache = Cache(backend=backend(filename=cache_filename))

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # create unique hash of function signature
            key = hashlib.sha1(
                (func.__name__ + str(args) + str(kwargs)).encode("utf-8")
            ).hexdigest()

            # get function result from cache
            res = cache[key]
            if res is None:
                # not yet in cache, get new result and store it in the cache
                res = func(*args, **kwargs)
                cache.set(key, res, ttl)
                if cache.is_persistent:
                    # if persistent, save new item to cache file
                    cache.save()

                log.debug(
                    "adding new cache entry for '{}({}, {})'".format(
                        func.__name__, args, kwargs
                    )
                )

            else:
                # existing function result from cache
                log.debug(
                    "getting existing cache entry for '{}({}, {})'".format(
                        func.__name__, args, kwargs
                    )
                )

            return res

        return wrapper

    return decorator


# decorator for memory backend
memorycache = partial(cache, backend=MemoryBackend)

# decorator for json backend
jsoncache = partial(cache, backend=JsonBackend)

# decorator for pickle backend
picklecache = partial(cache, backend=PickleBackend)
