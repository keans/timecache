from nose import tools

from timecache import Cache
from timecache.backends import MemoryBackend, NotPersistentException


# create cache with memory backend
cache = Cache(backend=MemoryBackend())


def test_simple_set():
    """
    simple testing of adding key, value pairs to the memory cache
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


@tools.raises(NotPersistentException)
def test_save_none_persistence():
    """
    this test should fail with NotPersistentException since the memory
    backend cannot persistently store the cache.
    """
    # try to save the cache which should fail
    cache.save()


@tools.raises(NotPersistentException)
def test_load_none_persistence():
    """
    this test should fail with NotPersistentException since the memory
    backend cannot persistently store the cache.
    """
    # try to load the cache which should fail
    cache.load()
