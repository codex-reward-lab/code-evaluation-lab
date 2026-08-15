"""Golden reference solution for the bounded TTL/LRU cache task."""

from collections import OrderedDict
from time import monotonic


class TTLCache:
    """A bounded least-recently-used cache with per-entry expiration."""

    def __init__(self, max_size, default_ttl=60.0, clock=None):
        if not isinstance(max_size, int) or isinstance(max_size, bool) or max_size <= 0:
            raise ValueError("max_size must be a positive integer")
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._clock = clock or monotonic
        self._data = OrderedDict()

    def set(self, key, value, ttl=None):
        lifetime = self.default_ttl if ttl is None else ttl
        expires_at = self._clock() + lifetime
        if key in self._data:
            del self._data[key]
        self._data[key] = (value, expires_at)
        self.prune_expired()
        while len(self._data) > self.max_size:
            self._data.popitem(last=False)

    def get(self, key, default=None):
        item = self._data.get(key)
        if item is None:
            return default
        value, expires_at = item
        if expires_at <= self._clock():
            del self._data[key]
            return default
        self._data.move_to_end(key)
        return value

    def prune_expired(self):
        now = self._clock()
        expired = [key for key, (_, expiry) in self._data.items() if expiry <= now]
        for key in expired:
            del self._data[key]
        return len(expired)

    def clear(self):
        self._data.clear()

    def __len__(self):
        self.prune_expired()
        return len(self._data)

    def __contains__(self, key):
        sentinel = object()
        return self.get(key, sentinel) is not sentinel
