from datetime import datetime
from functools import wraps

def processing_logger(log_file: str = "processing.log"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_entry = f"[{datetime.now()}] {func.__name__} success | args: {args}, kwargs: {kwargs}\n"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                return result
            except Exception as e:
                log_entry = f"[{datetime.now()}] {func.__name__} error: {str(e)} | args: {args}, kwargs: {kwargs}\n"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                raise
        return wrapper
    return decorator

def mask_logger(log_file: str = "masks.log"):
    def decorator(func):
        @wraps(func)
        def wrapper(number: str):
            try:
                result = func(number)
                log_entry = f"[{datetime.now()}] {func.__name__} success | input: {number}, output: {result}\n"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                return result
            except Exception as e:
                log_entry = f"[{datetime.now()}] {func.__name__} error: {str(e)} | input: {number}\n"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                return "Ошибка маскировки"  # Возвращаем понятное сообщение вместо исключения
        return wrapper
    return decorator

