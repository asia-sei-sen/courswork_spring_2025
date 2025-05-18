import sys
from datetime import (
    datetime,
)
from functools import (
    wraps,
)


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_entry = f"[{datetime.now()}] {func.__name__} ok | args: {args}, kwargs: {kwargs}, result: {result}\n"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_entry)
                else:
                    print(log_entry, file=sys.stdout)
                return result
            except Exception as e:
                log_entry = f"[{datetime.now()}] {func.__name__} error: {type(e).__name__} | args: {args}, kwargs: {kwargs}\n"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_entry)
                else:
                    print(log_entry, file=sys.stderr)
                raise
        return wrapper
    return decorator
