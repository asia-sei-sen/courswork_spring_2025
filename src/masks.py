def mask_credit_card(card_number: str) -> str:
    """Маскирует номер кредитной карты, оставляя первые 6 и последние 4 цифры."""
    card_number = card_number.replace(" ", "")
    if len(card_number) != 16 or not card_number.isdigit():
        return "Некорректный номер карты"
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def mask_account_number(account_number: str) -> str:
    """Маскирует номер счета, оставляя только последние 4 цифры."""
    account_number = account_number.replace(" ", "")
    if len(account_number) < 4 or not account_number.isdigit():
        return "Некорректный номер счета"
    return f"**{account_number[-4:]}"


from datetime import datetime


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата ISO в строку "ДД.ММ.ГГГГ".

    Args:
        date_str: Дата в формате "2024-03-11T02:26:18.671407"

    Returns:
        Строка с датой в формате "11.03.2024"

    Пример:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    try:
        # Парсим ISO-формат с временной зоной (если есть)
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return "Некорректный формат даты"