import os
from unittest.mock import mock_open, patch
from src.file_parsers.csv_parser import read_csv

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

def test_read_csv_mock():
    mock_csv = "date,amount,category\n2024-01-01,100,Food\n2024-01-02,200,Travel"
    with patch("builtins.open", mock_open(read_data=mock_csv)):
        result = read_csv("dummy_path.csv")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["category"] == "Food"

def test_read_csv_real_file():
    csv_file = os.path.join(DATA_DIR, "transactions.csv")
    result = read_csv(csv_file)
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], dict)
    assert "amount" in result[0]
