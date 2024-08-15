#!/usr/bin/env python3
""" Redis Module Cache and Tracking """

import redis
import requests
from functools import wraps
from typing import Callable


# Create a Redis connection instance
redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator for counting requests and caching results."""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function for caching and counting."""
        # Increment the request count for the URL
        redis_client.incr(f"count:{url}")

        # Check if the URL's content is already cached
        cached_html = redis_client.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # If not cached, fetch the content and cache it
        html = method(url)
        redis_client.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Obtain the HTML content of a URL."""
    response = requests.get(url)
    return response.text
