==============
 timecache
==============

`timecache` is a timeout-based cache implementation for Python 3.x without
any external dependencies. Depending on the selected backend, the cache can be
made persistent to survive a fresh start of a script (currently, json and
pickle files are supported as backend).

Warning: this is an early alpha version so the interface may change in future
versions.


Setup
-----

Install `timecache` using `pip`:

::

    pip install -U timecache


Example
-------

A cache with a memory backend can be created as follows:

::

    import time
    from timecache import Cache, FIVE_SECONDS

    # create cache with memory backend
    cache = Cache()

    # add a value to the cache with a default duration of 1 minute
    cache["one"] = 1

    # add a value to the cache with a duration of 5 seconds
    cache.set("two", 2, FIVE_SECONDS)

    print("two in cache: {}".format("two" in cache))

    # show cache entry
    print(cache)

    # wait for 6 s
    time.sleep(6)

    # show cache entry
    print(cache)

    print("two in cache: {}".format("two" in cache))


A cache with a json file backend can be created as follows:

::

    import time
    from timecache import Cache, JsonBackend, FIVE_SECONDS

    # create cache with json backend
    cache = Cache(backend=JsonBackend())

    if not cache.is_existing:
        # add a value to the cache with a default duration of 1 minute
        print("adding new value to the cache...")
        cache["one"] = 1
        print("savíng cache to file '{}'".format(cache.filename))
        cache.save()

    # show cache entry
    print(cache)

When calling the script again the cached value will be loaded from the
json file.


Testing
-------

For testing additionally install `nose` and then run the tests:

::

    pip install nose
    nosetests


Hint
----

If you do not need a time-based cache, consider the `lru_cache` function of
Python's `functools` module
(https://docs.python.org/3/library/functools.html).
