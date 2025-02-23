from redis import asyncio as aioredis

REDIS_URL = "redis://localhost"


async def get_redis():
    return await aioredis.from_url(REDIS_URL, decode_responses=True)
