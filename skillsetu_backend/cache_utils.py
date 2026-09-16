from functools import wraps
from django.core.cache import cache
import hashlib
import json

def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    raw_payload = json.dumps({"args": [str(a) for a in args], "kwargs": {k: str(v) for k, v in sorted(kwargs.items())}}, sort_keys=True)
    digest = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()[:16]
    return f"skillsetu:{prefix}:{digest}"

def get_cached(key: str):
    try:
        return cache.get(key)
    except Exception:
        return None

def set_cached(key: str, value, timeout: int = 300):
    try:
        cache.set(key, value, timeout)
    except Exception:
        pass

def invalidate_cache_keys(*keys):
    try:
        for k in keys:
            cache.delete(k)
    except Exception:
        pass

def invalidate_by_prefix(prefix: str):
    try:
        if hasattr(cache, "_cache"):
            matching = [k for k in list(cache._cache.keys()) if prefix in str(k)]
            for k in matching:
                if hasattr(cache, "_delete"):
                    cache._delete(k)
                else:
                    cache.delete(k)
    except Exception:
        pass
