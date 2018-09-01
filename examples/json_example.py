#!/usr/bin/env python
# -*- coding: utf-8 -*-

from timecache import Cache, JsonBackend, ONE_MINUTE, FIVE_MINUTES, \
    FIFTEEN_MINUTES


def main():
    # create cache with json backend
    cache = Cache(backend=JsonBackend())

    if not cache.is_existing:
        # create a new cache, add three key, value pairs with different
        # caching durations and save them persistently as json file

        print("creating new cache...")
        cache.set("one", 1, ONE_MINUTE)
        cache.set("two", 2, FIVE_MINUTES)
        cache.set("three", 3, FIFTEEN_MINUTES)
        cache.set("four", 4)

        print("saving cache to '{}'...".format(cache.filename))
        cache.save()
        print(cache)

    else:
        # auto-loaded existing cache from file
        print("existing cache from '{}'.".format(cache.filename))
        print(cache)


if __name__ == "__main__":
    main()
