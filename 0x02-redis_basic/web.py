#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """


import redis
from typing import Callable
import requests
from functools import wraps


def track_get_page(fn: Callable) -> Callable:
    """
    Implementing an expiring web cache and tracker
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        redisClient = redis.Redis()
        redisClient.incr(f'count:{url}')
        cachedPage = redisClient.get(f'{url}')

        if cachedPage:
            return cachedPage.decode('utf-8')
        response = fn(url)
        redisClient.setex(f'{url}', 10, response)
        return response

    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    Http request
    """
    response = requests.get(url)
    return response.text
