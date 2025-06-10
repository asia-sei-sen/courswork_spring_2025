import os
import json
import pytest
import pandas as pd
from src.invest_savings import (
    read_transactions_from_excel,
    investkopilka,
    run_invest_savings
)


EXCEL_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/operations.xlsx')


@pytest.fixture
def sample_transactions():
    return [
        {"date": "2025-05-01", "amount": 100.50},
        {"date": "2025-05-02", "amount": 200.75},
        {"date": "2025-05-03", "amount": 300.00}
    ]


def test_read_real_excel_file():
    if not os.path.exists(EXCEL_FILE_PATH):
        pytest.skip(f"Файл {EXCEL_FILE_PATH} не найден")
    transactions = read_transactions_from_excel(EXCEL_FILE_PATH)
    assert isinstance(transactions, list)
    assert len(transactions) > 0
    assert all("date" in t and "amount" in t for t in transactions)


def test_run_with_real_excel_file():
    if not os.path.exists(EXCEL_FILE_PATH):
        pytest.skip(f"Файл {EXCEL_FILE_PATH} не найден")
    result = run_invest_savings(EXCEL_FILE_PATH, "2025-05", 10)
    data = json.loads(result)
    assert isinstance(data, dict)
    assert "month" in data
    assert "round_limit" in data
    assert "total_round_up" in data


def test_read_transactions_success(tmp_path):
    df = pd.DataFrame({
        "date": ["2025-05-01", "2025-05-15"],
        "amount": [100.0, 150.5]
    })
    test_file = tmp_path / "test.xlsx"
    df.to_excel(test_file, index=False)

    transactions = read_transactions_from_excel(str(test_file))
    assert len(transactions) == 2
    assert transactions[0]["amount"] == 100.0


def test_read_transactions_missing_columns(tmp_path):
    df = pd.DataFrame({"wrong_column": [1, 2]})
    test_file = tmp_path / "invalid.xlsx"
    df.to_excel(test_file, index=False)

    transactions = read_transactions_from_excel(str(test_file))
    assert transactions == []


def test_investkopilka_normal_case(sample_transactions):
    result = investkopilka("2025-05", sample_transactions, 10)
    data = json.loads(result)
    assert data["total_round_up"] == 1.25  # 0.50 + 0.75


def test_investkopilka_empty_transactions():
    result = investkopilka("2025-05", [], 10)
    data = json.loads(result)
    assert data["total_round_up"] == 0


def test_investkopilka_invalid_data():
    transactions = [{"date": "invalid", "amount": "text"}]
    result = investkopilka("2025-05", transactions, 10)
    assert "error" in json.loads(result)


def test_run_invest_savings_success(tmp_path):
    df = pd.DataFrame({
        "date": ["2025-05-01", "2025-05-02"],
        "amount": [100.50, 200.75]
    })
    test_file = tmp_path / "test_run.xlsx"
    df.to_excel(test_file, index=False)

    result = run_invest_savings(str(test_file), "2025-05", 10)
    data = json.loads(result)
    assert data["total_round_up"] == 1.25


def test_run_invest_savings_invalid_path():
    result = run_invest_savings("nonexistent.xlsx", "2025-05", 10)
    assert json.loads(result) == []
