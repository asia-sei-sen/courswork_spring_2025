"""Тесты для модуля processing."""
import pytest
from src.processing import sort_by_date

@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {"date": "2023-08-20T12:00:00", "amount": 100},
        {"date": "2022-05-15T08:30:00", "amount": 200},
        {"date": "2023-01-10T16:45:00", "amount": 300},
        {"date": "invalid_date", "amount": 400},  # Некорректная дата
    ]

def test_sort_descending(sample_transactions):
    """Тест сортировки по убыванию даты (новые сначала)."""
    result = sort_by_date(sample_transactions, reverse=True)
    dates = [t["date"] for t in result if t["date"] != "invalid_date"]
    assert dates == ["2023-08-20T12:00:00", "2023-01-10T16:45:00", "2022-05-15T08:30:00"]

def test_sort_ascending(sample_transactions):
    """Тест сортировки по возрастанию даты (старые сначала)."""
    result = sort_by_date(sample_transactions, reverse=False)
    dates = [t["date"] for t in result if t["date"] != "invalid_date"]
    assert dates == ["2022-05-15T08:30:00", "2023-01-10T16:45:00", "2023-08-20T12:00:00"]

def test_invalid_dates_placed_last(sample_transactions):
    """Тест, что транзакции с некорректными датами идут последними."""
    result = sort_by_date(sample_transactions, reverse=True)
    assert result[-1]["date"] == "invalid_date"

def test_empty_list():
    """Тест обработки пустого списка."""
    assert sort_by_date([]) == []

def test_single_transaction():
    """Тест обработки списка с одной транзакцией."""
    single = [{"date": "2023-01-01T00:00:00", "amount": 100}]
    assert sort_by_date(single) == single

@pytest.mark.parametrize("reverse,expected", [
    (True, ["2023-08-20", "2023-01-10", "2022-05-15"]),
    (False, ["2022-05-15", "2023-01-10", "2023-08-20"])
])
def test_parametrized_sorting(reverse, expected):
    """Параметризованный тест сортировки."""
    transactions = [
        {"date": f"{date}T00:00:00", "amount": 100} for date in expected[::-1]
    ]
    result = sort_by_date(transactions, reverse=reverse)
    assert [t["date"][:10] for t in result] == expected