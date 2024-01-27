#!/usr/bin/env python3
""" Writing strings to Redis """


import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """  Incrementing values """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ generate a key """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ generate keys for inputs and outputs """
    inputKey = method.__qualname__ + ":inputs"
    outputKey = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ generate keys for inputs and outputs """
        self._redis.rpush(inputKey, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputKey, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """ Generate keys for inputs and outputs """
    inputs_key = "{}:inputs".format(method.__qualname__)
    outputs_key = "{}:outputs".format(method.__qualname__)
    inputs_history = method.__self__._redis.lrange(inputs_key, 0, -1)
    outputs_history = method.__self__._redis.lrange(outputs_key, 0, -1)

    print("{} was called {} times:".format(
        method.__qualname__, len(inputs_history)))

    for inputs, output in zip(inputs_history, outputs_history):
        print("{}(*{}) -> {}".format(
            method.__qualname__,
            inputs.decode("utf-8"), output.decode("utf-8")))


class Cache:
    """ Cache class """
    def __init__(self):
        """ Initialize redis & flush db """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generate random key"""
        rKey = str(uuid.uuid4())
        self._redis.set(rKey, data)

        return rKey

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """ retrieve data """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Cache.get with str conversion func """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """ Cache.get with int conversion func """
        return self.get(key, fn=int)
