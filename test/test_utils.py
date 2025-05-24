import pytest
import json
from unittest.mock import mock_open, patch
from src.utils import load_transactions


def test_load_transactions_valid_json():
    # Подготовка поддельных данных
    mock_data = json.dumps([
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "RUB"}
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)), \
         patch("os.path.exists", return_value=True):
        result = load_transactions("fake_path.json")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["amount"] == 100


def test_load_transactions_file_not_found():
    with patch("os.path.exists", return_value=False):
        result = load_transactions("nonexistent.json")
    assert result == []


def test_load_transactions_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")), \
         patch("os.path.exists", return_value=True):
        result = load_transactions("invalid.json")
    assert result == []


def test_load_transactions_not_a_list():
    mock_data = json.dumps({"id": 1, "amount": 100})
    with patch("builtins.open", mock_open(read_data=mock_data)), \
         patch("os.path.exists", return_value=True):
        result = load_transactions("notalist.json")
    assert result == []
