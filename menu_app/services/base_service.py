"""Модуль используется для инициализации методов кэширования в слое."""
import pickle
from typing import Any

import aioredis
from celery import Celery

from menu_app.config import config

celery_app = Celery('menu_app', broker=f'redis://{config.REDIS_HOST}')


class BaseService:
    """Базовый класс сервисных операций."""

    def __init__(self):
        """Инициализация базовых значений адреса redis и времени жизни кэша."""
        self.url_redis = f'redis://{config.REDIS_HOST}/1'
        self.cache_lifetime = 60

    async def set_cache(self, request: str, response: Any) -> None:
        """
        Функция задает значение кэша с ключом request и значением результата\
        запроса.

        :param request: Ключ запроса.
        :param response: Ответ, полученный на запрос от базы данных.
        :return: None.
        """
        response = pickle.dumps(response)
        async with aioredis.from_url(self.url_redis) as redis:
            await redis.set(request, response, ex=self.cache_lifetime)

    async def get_cache(self, request: str) -> Any:
        """
        Функция получает из кэша значение запроса к базе данных.

        :param request: Ключ запроса.
        :return: Декодированные данные.
        """
        async with aioredis.from_url(self.url_redis) as redis:
            cache = await redis.get(request)
        if cache:
            cache = pickle.loads(cache)
        return cache

    async def delete_cache(self, request: list[str]) -> None:
        """
        Функция удаляет записи кэша всех передаваемых ключей.

        :param request: Список ключей запроса для удаления.
        :return:None.
        """
        async with aioredis.from_url(self.url_redis) as redis:
            await redis.delete(*request)

    async def get_keys_by_patterns(self, pattern: str) -> list:
        async with aioredis.from_url(self.url_redis) as redis:
            return await redis.keys(pattern)

    async def flush_redis(self) -> None:
        """
        Очищает весь кэш из redis.

        :return: None.
        """
        async with aioredis.from_url(self.url_redis) as redis:
            await redis.flushdb(asynchronous=True)
