#!/usr/bin/env python3
"""Module for caching data using Redis."""

import redis
from typing import Union, Callable, Optional, Any
from uuid import uuid4


class Cache:
    """Class for caching data."""

    def __init__(self) -> None:
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the cache.

        Args:
            data (Union[str, bytes, int, float]): Data to be stored.

        Returns:
            str: The key under which the data is stored.
        """
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[Any], Any]]) -> Any:
        """Retrieve data from cache and apply a function if provided."""
        result: Any = self._redis.get(key)
        if fn is int:
            return int(result)
        elif fn is str:
            return str(result)
        else:
            return result
        
    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string value from cache."""
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer value from cache."""
        return self.get(key, int)

