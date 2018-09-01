import os
import json
import datetime

from ..cachentry import CacheEntry
from .filebackend import FileBackend


class JsonCacheEncoder(json.JSONEncoder):
    """
    custom json encoder that allows the storing of CacheEntry objects
    """
    def default(self, obj):
        if isinstance(obj, CacheEntry):
            # --- cache entry ---
            return {
                "creation_time": obj.creation_time.isoformat(),
                "duration": [
                    obj.duration.days,
                    obj.duration.seconds,
                    obj.duration.microseconds,
                ],
                "value": obj.value,
            }

        # let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class JsonCacheDecoder(json.JSONDecoder):
    """
    custom json decoder that allows the loading of CacheEntry objects
    """
    def __init__(self, *args, **kargs):
        json.JSONDecoder.__init__(
            self, object_hook=self._dict_to_object, *args, **kargs
        )

    def _dict_to_object(self, d):
        if ("creation_time" in d) and ("duration" in d) and ("value" in d):
            # --- cache entry ---
            ce = CacheEntry(
                value=d["value"],
                duration=datetime.timedelta(*d["duration"])
            )
            ce.creation_time = datetime.datetime.strptime(
                d["creation_time"], "%Y-%m-%dT%H:%M:%S.%f"
            )

            return ce

        return d


class JsonBackend(FileBackend):
    """
    backend to store and load cached data from json file
    """
    def __init__(self, filename=None):
        FileBackend.__init__(self)
        self.filename = filename or "cache.json"

    def load(self):
        """
        load cached data from json file
        """
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f, cls=JsonCacheDecoder)

        return None

    def save(self, data):
        """
        save cached data to json file
        """
        with open(self.filename, "w") as f:
            json.dump(data, f, cls=JsonCacheEncoder)
