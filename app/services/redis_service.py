from fastapi import HTTPException

TTL = 3600


class RedisService:
    async def add_token(
        self,
        redis_db,
        token: str,
        login_id: str,
    ):
        await redis_db.set(token, login_id, ex=TTL)

    async def delete_token(self, redis_db, token):

        value = await redis_db.get(token)
        if value is None:
            raise HTTPException(status_code=404, detail="Redis token expired")

        await redis_db.delete(token)
