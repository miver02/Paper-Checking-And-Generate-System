from django_redis import get_redis_connection
from rest_framework.exceptions import Throttled
from pathlib import Path

# 读取 Lua 脚本
LUA_SCRIPT = Path(__file__).resolve().parent.parent / "lua" / "rate_limit.lua"

with open(LUA_SCRIPT, "r") as f:
    RATE_LIMIT_LUA = f.read()


class RedisRateLimitService:
    """
    Redis + Lua 原子限流
    """

    _lua_sha = None

    @classmethod
    def check(cls, key: str, limit: int, window: int):
        conn = get_redis_connection("default")

        if cls._lua_sha is None:
            cls._lua_sha = conn.script_load(RATE_LIMIT_LUA)
        
        try:
            allowed = conn.evalsha(
                cls._lua_sha,
                1,
                key,
                limit,
                window,
            )
        except Exception:
            # Lua 丢失时自动重载
            cls._lua_sha = conn.script_load(RATE_LIMIT_LUA)
            allowed = conn.evalsha(
                cls._lua_sha,
                1,
                key,
                limit,
                window,
            )

        if allowed == 0:
            raise Throttled(detail="请求过于频繁，请稍后再试")
