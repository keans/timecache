from datetime import timedelta

# some pre-defined names for durations
ONE_SECOND = timedelta(seconds=1)
FIVE_SECONDS = timedelta(seconds=5)
TEN_SECONDS = timedelta(seconds=10)
FIFTEEN_SECONDS = timedelta(seconds=15)
THIRTY_SECONDS = timedelta(seconds=30)
ONE_MINUTE = timedelta(minutes=1)
FIVE_MINUTES = timedelta(minutes=5)
TEN_MINUTES = timedelta(minutes=10)
FIFTEEN_MINUTES = timedelta(minutes=15)
THIRTY_MINUTES = timedelta(minutes=30)
FORTYFIVE_MINUTES = timedelta(minutes=45)
ONE_HOUR = timedelta(hours=1)
ONE_DAY = timedelta(days=1)
ONE_WEEK = timedelta(weeks=1)

# stay forever in the cache until manually deleted
FOREVER = None

# default duration of a cache entry
DEFAULT_DURATION = ONE_MINUTE
