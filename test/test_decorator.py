import os

import pytest

from decorators.log import (
    log,
)

LOG_FILE = "test_log.log"


# Очистка лог-файла перед тестами
def setup_module(module):
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


# Примерная функция для тестирования
@log(filename=LOG_FILE)
def successful_function(x, y):
    return x + y


@log(filename=LOG_FILE)
def error_function(x, y):
    raise ValueError("Test Error")


def test_successful_log_to_file():
    # Вызов функции
    result = successful_function(2, 3)
    assert result == 5

    # Проверка содержимого лог-файла
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.readlines()

    assert len(logs) == 1
    assert "successful_function ok" in logs[0]
    assert "args: (2, 3)" in logs[0]
    assert "result: 5" in logs[0]


def test_error_log_to_file():
    with pytest.raises(ValueError):
        error_function(2, 3)

    # Проверка содержимого лог-файла
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.readlines()

    # Логов должно быть два: успешное выполнение и ошибка
    assert len(logs) == 2
    assert "error_function error" in logs[1]
    assert "ValueError" in logs[1]
    assert "args: (2, 3)" in logs[1]


def test_log_to_console(capsys):
    # Тест без указания файла
    @log()
    def console_function(x, y):
        return x - y

    console_function(10, 5)
    captured = capsys.readouterr()
    assert "console_function ok" in captured.out


def teardown_module(module):
    """Удаляет лог-файл после выполнения тестов"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
