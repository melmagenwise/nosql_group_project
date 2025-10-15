# Exercice 8.3.a: cache.py
import os
import json
import redis

# Redis URL (env)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Client
r = redis.from_url(REDIS_URL, decode_responses=True)

# Default TTL (seconds)
DEFAULT_TTL = int(os.getenv("CACHE_TTL_SECONDS", "120"))

# Get value for key
def get(key):
    try:
        return r.get(key)
    except redis.RedisError:
        return None

# Set value with TTL
def set(key, value, ttl = DEFAULT_TTL):
    try:
        return bool(r.set(key, value, ex=ttl))
    except redis.RedisError:
        return False

# Delete key
def delete(key):
    try:
        r.delete(key)
    except redis.RedisError:
        pass

# Get JSON value
def get_json(key):
    raw = get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None

# Set JSON value with TTL
def set_json(key, obj, ttl = DEFAULT_TTL):
    try:
        return set(key, json.dumps(obj), ttl=ttl)
    except Exception:
        return False

# Delete keys by prefix
def delete_prefix(prefix):
    try:
        pipe = r.pipeline()
        for k in r.scan_iter(match=f"{prefix}*"):
            pipe.delete(k)
        pipe.execute()
    except redis.RedisError:
        pass

# Ping server
def ping():
    try:
        return bool(r.ping())
    except redis.RedisError:
        return False
