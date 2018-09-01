import os

from timecache import Cache
from timecache.backends import PickleBackend

# used for testing the persistence of the cache
TEST_CACHE_FILENAME = "/tmp/test_pickle_cache.dat"

# create cache with pickle backend
cache = Cache(backend=PickleBackend(filename=TEST_CACHE_FILENAME))


def test_simple_set():
    """
    simple testing of adding key, value pairs to the pickle cache
    and loading them
    """
    # put some key value pairs into the cache
    cache.set("one", 1)
    cache.set("two", 2)
    cache.set("three", 3)

    # make sure that they can be obtained
    assert("two" in cache)
    assert(cache.get("two").value == 2)
    assert(cache.get("three").value == 3)
    assert(cache.get("one").value == 1)
    assert(cache["one"].value == 1)
    assert("four" not in cache)
    assert(cache.get("four") is None)

    # check len when removing an item
    assert(len(cache) == 3)
    cache.remove("one")
    assert(len(cache) == 2)


def test_persistence():
    """
    save some values in the pickle cache file and then load them again
    """
    # put some key value pairs into the cache
    cache.set("one", 1)
    cache.set("two", 2)
    cache.set("three", 3)

    cache.save()

    # create a new cache instance with pickle backend
    cache2 = Cache(backend=PickleBackend(filename=TEST_CACHE_FILENAME))
    cache2.load()

    # make sure that they can be obtained
    assert(cache2.get("two").value == 2)
    assert(cache2.get("three").value == 3)
    assert(cache2.get("one").value == 1)
    assert(cache2["one"].value == 1)
    assert(cache2.get("four") is None)

    # remove temporary file
    os.remove(TEST_CACHE_FILENAME)
