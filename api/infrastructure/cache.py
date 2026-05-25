import json
from typing import Any, Optional

class RedisCache:
    """Mock Redis caching layer for heavy intelligence operations."""
    
    def __init__(self):
        self._store = {}
        self.hits = 0
        self.misses = 0
        self.invalidations = 0

    async def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            self.hits += 1
            return json.loads(self._store[key])
        self.misses += 1
        return None

    async def set(self, key: str, value: Any, expire_seconds: int = 3600):
        self._store[key] = json.dumps(value)

    async def invalidate(self, pattern: str):
        # Mock pattern invalidation
        keys_to_delete = [k for k in self._store.keys() if pattern in k]
        for k in keys_to_delete:
            del self._store[k]
            self.invalidations += 1

    def get_telemetry(self) -> dict:
        total = self.hits + self.misses
        hit_ratio = (self.hits / total * 100) if total > 0 else 0
        return {
            "hit_ratio": f"{hit_ratio:.1f}%",
            "total_keys": len(self._store),
            "invalidations": self.invalidations
        }

redis_client = RedisCache()
