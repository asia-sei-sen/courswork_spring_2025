import pytest
from unittest.mock import patch, MagicMock
from src import main as main_module
import os


def test_main_json(monkeypatch, capsys, tmp_path):
    # Подготовка тестовых данных JSON
    test_data = [
        {
            "date": "2024-04-10T10:30:00",
            "state": "EXECUTED",
            "description": "оплата услуги",
            "from": "Счет 40817810099910004312",
            "to": "Maestro 1596837868705199",
            "operationAmount": {
                "amount": "1000",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        },
        {
            "date": "2024-04-11T12:00:00",
            "state": "CANCELLED",
            "description": "перевод на карту",
            "from": "Счет 40817810000000000000",
            "to": "Visa 1234567890123456",
            "operationAmount": {
                "amount": "2000",
                "currency": {
                    "name": "RUB",
                    "code": "RUB"
                }
            }
        }
    ]

    # Моки
    monkeypatch.setattr(main_module, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(main_module, "FILENAME", "transactions.json")

    with patch("src.main.load_json_file", return_value=test_data), \
            patch("src.main.convert_to_rub", return_value=1234.56):
        main_module.main()

    captured = capsys.readouterr()
    assert "Загружено транзакций: 2" in captured.out
    assert "оплата услуги" in captured.out
    assert "1234.56 RUB" in captured.out
    assert "Категории:" in captured.out
    assert "→" in captured.out


def test_main_invalid_format(monkeypatch):
    monkeypatch.setattr(main_module, "DATA_DIR", ".")
    monkeypatch.setattr(main_module, "FILENAME", "transactions.txt")
    with pytest.raises(ValueError, match="Неподдерживаемый формат файла"):
        main_module.main()
