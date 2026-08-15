"""Candidate baseline for the bounded TTL/LRU cache task."""


class TTLCache:
    """A deliberately incomplete baseline that only supports basic storage."""

    def __init__(self, max_size, default_ttl=60.0, clock=None):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._data = {}

    def set(self, key, value, ttl=None):
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def prune_expired(self):
        return 0

    def clear(self):
        self._data.clear()

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data
