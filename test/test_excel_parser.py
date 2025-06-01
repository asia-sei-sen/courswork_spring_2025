import os
import pandas as pd
from unittest.mock import patch
from src.file_parsers.excel_parser import read_excel

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

def test_read_excel_mock():
    # Мок DataFrame, чтобы не читать реальный файл
    data = {'date': ['2024-01-01'], 'amount': [100], 'category': ['Food']}
    df_mock = pd.DataFrame(data)

    with patch('pandas.read_excel', return_value=df_mock):
        result = read_excel("dummy_path.xlsx")
        assert isinstance(result, list)
        assert result[0]['category'] == 'Food'

def test_read_excel_real_file():
    # Тест с настоящим файлом из test/data
    excel_file = os.path.join(DATA_DIR, "transactions_excel.xlsx")
    result = read_excel(excel_file)
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], dict)
    assert 'amount' in result[0]
