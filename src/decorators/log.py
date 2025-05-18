import sys
from datetime import (
    datetime,
)
from functools import (
    wraps,
)

def log(filename=None):
    """
    Декоратор для логирования выполнения функции.

    Логирует начало и конец выполнения функции, а также её результат или возникшие ошибки.
    Логи могут записываться либо в указанный файл, либо выводиться в консоль.

    Args:
        filename (str, optional): Имя файла для записи логов.
                                  Если None, логи выводятся в консоль.

    Returns:
        function: Обернутая функция с логированием.

    Пример использования:
        @log(filename="log.txt")
        def add(a, b):
            return a + b

        add(2, 3)
        # В log.txt:
        # [2025-05-20 14:33:01.123456] add ok | args: (2, 3), kwargs: {}, result: 5
    """
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
