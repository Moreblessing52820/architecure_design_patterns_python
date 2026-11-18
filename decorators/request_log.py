from flask import request
from datetime import datetime
from functools import wraps
from functools import wraps


class RequestStats:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.count = 0
            cls._instance.last_path = None
            cls._instance.last_seconds = None

        return cls._instance


REQUESTS = RequestStats()


def request_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        started = datetime.now()
        REQUESTS.count += 1
        REQUESTS.last_path = request.path

        try:
            return func(*args, **kwargs)
        finally:
            REQUESTS.last_seconds = (
                datetime.now() - started
            ).total_seconds()

            print(
                "request",
                REQUESTS.count,
                request.path,
                REQUESTS.last_seconds
            )

    return wrapper