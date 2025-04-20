"""Тесты для модуля маскировки банковских карт и счетов."""

from src.masks import mask_credit_card, mask_account_number

def test_card_masking():
    """Тест маскировки номера карты."""
    assert mask_credit_card("1234567890123456") == "1234 56** **** 3456"
    assert mask_credit_card("1234 5678 9012 3456") == "1234 56** **** 3456"
    assert mask_credit_card("1234") == "Некорректный  номер карты"

def test_account_masking():
    """Тест маскировки номера счета."""
    assert mask_account_number("1234567890") == "**7890"
    assert mask_account_number("1234 5678 90") == "**7890"
    assert mask_account_number("123") == "Некорректный номер счета"