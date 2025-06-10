from datetime import datetime
from unittest.mock import patch
from src.utils import (
    get_greeting,
    get_card_summary,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
    prepare_main_page_response,
)


def test_get_greeting():
    assert get_greeting(datetime.strptime("2025-06-09 06:00:00", "%Y-%m-%d %H:%M:%S")) == "Доброе утро"
    assert get_greeting(datetime.strptime("2025-06-09 13:00:00", "%Y-%m-%d %H:%M:%S")) == "Добрый день"
    assert get_greeting(datetime.strptime("2025-06-09 19:00:00", "%Y-%m-%d %H:%M:%S")) == "Добрый вечер"
    assert get_greeting(datetime.strptime("2025-06-09 23:30:00", "%Y-%m-%d %H:%M:%S")) == "Доброй ночи"


def test_get_card_summary():
    transactions = [
        {"card_number": "1234567890123456", "amount": -150.0},
        {"card_number": "1234567890123456", "amount": -250.0},
        {"card_number": "9876543210987654", "amount": -99.99},
        {"card_number": "9876543210987654", "amount": 200.0},
        {"card_number": "1111222233334444", "amount": 100.0},
    ]
    summary = get_card_summary(transactions)
    assert isinstance(summary, list)
    assert len(summary) == 2  # только две карты с расходами
    for card in summary:
        assert "card_last4" in card
        assert "total_spent" in card
        assert "cashback" in card
        assert isinstance(card["cashback"], int)
        assert card["total_spent"] > 0


def test_get_card_summary_missing_columns(caplog):
    transactions = [{"wrong_key": 1}]
    result = get_card_summary(transactions)
    assert result == []
    assert any("нет нужных колонок" in record.message for record in caplog.records)


def test_get_top_transactions():
    transactions = [
        {"date": "2025-06-01", "amount": 100, "description": "desc1"},
        {"date": "2025-06-02", "amount": -300, "description": "desc2"},
        {"date": "2025-06-03", "amount": 50},
        {"date": "2025-06-04", "amount": -200},
        {"date": "2025-06-05", "amount": 400},
        {"date": "2025-06-06", "amount": -10},
    ]
    top = get_top_transactions(transactions, top_n=3)
    assert len(top) == 3
    amounts = [abs(t["amount"]) for t in top]
    assert amounts == sorted(amounts, reverse=True)
    for t in top:
        assert "date" in t
        assert "amount" in t


def test_get_top_transactions_missing_amount(caplog):
    transactions = [{"date": "2025-06-01"}]
    result = get_top_transactions(transactions)
    assert result == []
    assert any("нет колонки 'amount'" in record.message for record in caplog.records)


@patch("src.utils.requests.get")
def test_get_currency_rates_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "Valute": {
            "USD": {"Value": 74.0},
            "EUR": {"Value": 90.0},
            "CNY": {"Value": 11.5},
        }
    }
    rates = get_currency_rates()
    assert rates == {"USD": 74.0, "EUR": 90.0, "CNY": 11.5}


@patch("src.utils.requests.get")
def test_get_currency_rates_failure(mock_get, caplog):
    mock_get.side_effect = Exception("Network error")
    rates = get_currency_rates()
    assert rates == {}
    assert any("Ошибка получения курсов валют" in record.message for record in caplog.records)


def test_get_stock_prices():
    prices = get_stock_prices()
    assert isinstance(prices, dict)
    for ticker in ["AAPL", "MSFT", "GOOGL"]:
        assert ticker in prices
        assert isinstance(prices[ticker], float)


def test_prepare_main_page_response(monkeypatch):
    transactions = [
        {"card_number": "1234567890123456", "amount": -150.0},
        {"card_number": "1234567890123456", "amount": -250.0},
        {"card_number": "9876543210987654", "amount": -99.99},
        {"date": "2025-06-01", "amount": 100, "description": "desc1"},
        {"date": "2025-06-02", "amount": -300, "description": "desc2"},
    ]

    monkeypatch.setattr("src.utils.get_currency_rates", lambda: {"USD": 74.0, "EUR": 90.0, "CNY": 11.5})
    monkeypatch.setattr("src.utils.get_stock_prices", lambda: {"AAPL": 170.33, "MSFT": 320.45})

    response_json = prepare_main_page_response("2025-06-09 12:00:00", transactions)
    import json

    response = json.loads(response_json)

    assert "greeting" in response
    assert "cards" in response
    assert "top_transactions" in response
    assert "currency_rates" in response
    assert "stock_prices" in response
    assert response["greeting"] == "Добрый день"


def test_prepare_main_page_response_invalid_date(monkeypatch, caplog):
    monkeypatch.setattr("src.utils.get_currency_rates", lambda: {})
    monkeypatch.setattr("src.utils.get_stock_prices", lambda: {})
    response_json = prepare_main_page_response("invalid date", [])
    import json

    response = json.loads(response_json)
    assert "greeting" in response
    assert response["cards"] == []
