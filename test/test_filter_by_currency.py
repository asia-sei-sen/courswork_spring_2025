# test/test_filter_by_currency.py
from generators import (
    filter_by_currency,
)


def test_filter_by_currency_with_matching_currency():
    # Arrange
    transactions = [
        {
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            },
            "description": "Payment 1"
        },
        {
            "operationAmount": {
                "currency": {
                    "code": "EUR"
                }
            },
            "description": "Payment 2"
        }
    ]

    # Act
    result = list(filter_by_currency(transactions, "USD"))

    # Assert
    assert len(result) == 1
    assert result[0]["description"] == "Payment 1"
    assert result[0]["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_with_non_matching_currency():
    # Arrange
    transactions = [
        {
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            },
            "description": "Payment 1"
        }
    ]

    # Act
    result = list(filter_by_currency(transactions, "EUR"))

    # Assert
    assert len(result) == 0


def test_filter_by_currency_with_empty_list():
    # Arrange
    transactions = []

    # Act
    result = list(filter_by_currency(transactions, "USD"))

    # Assert
    assert len(result) == 0


def test_filter_by_currency_returns_iterator():
    # Arrange
    transactions = [
        {
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            }
        }
    ]

    # Act
    result = filter_by_currency(transactions, "USD")

    # Assert
    assert hasattr(result, '__iter__')
    assert not hasattr(result, '__len__')  # Проверяем что это именно итератор, а не список