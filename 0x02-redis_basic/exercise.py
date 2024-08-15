#!/usr/bin/env python3
"""Module for caching data using Redis."""

import redis
from functools import wraps
from typing import Union, Callable, Optional, Any
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method and
       increment the count in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Decorator to count the number of calls to a method and
            increment the count in Redis.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to log inputs and outputs of a method to Redis.

    Args:
        method (Callable): The method to be wrapped.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """"Logs inputs and outputs of a method to Redis."""
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", result)
        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Replay the method calls stored in Redis.

    Args:
        method (Callable): The method to replay.
    """
    method_name = method.__qualname__
    redis_db = method.__self__._redis
    inputs = [input.decode("utf-8")
              for input in redis_db.lrange(f"{method_name}:inputs", 0, -1)]
    outputs = [output.decode("utf-8")
               for output in redis_db.lrange(f"{method_name}:outputs", 0, -1)]

    print(f"{method_name} was called {len(inputs)} times:")
    for input_val, output_val in zip(inputs, outputs):
        print(f"{method_name}(*{input_val}) -> {output_val}")


class Cache:
    """Class for caching data."""

    def __init__(self) -> None:
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

    def get(self, key: str, fn: Optional[Callable[[Any], Any]] = None) -> Any:
        """Retrieve data from cache and apply a function if provided."""
        result: Any = self._redis.get(key)
        return result if fn is None or result is None else fn(result)

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string value from cache."""
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer value from cache."""
        return self.get(key, int)
