import os

import redis
import json


class RedisBooks:
    redis = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), decode_responses=True)

    @classmethod
    def save(cls, user_id, book_data):
        cls.redis.hset(f'user_{user_id}', f'book_{book_data.get("id")}', json.dumps(book_data))

    @classmethod
    def retrieve(cls, user_id):
        book = cls.redis.hgetall(f'user_{user_id}').values()
        if not book:
            return None
        return [json.loads(i) for i in book]

    @classmethod
    def delete(cls, user_id, book_id):
        cls.redis.hdel(f'user_{user_id}', f'book_{book_id}')