import re
from src.maskc import mask_credit_card, mask_account_number


def mask_account_card(info: str) -> str:
    """
    Маскирует номер карты или счета, сохраняя исходное название/тип.

    Args:
        info: Строка формата "Visa Platinum 7000792289606361" или "Счет 73654108430135874305".

    Returns:
        Строка с маскированным номером карты/счета, например:
        - "Visa Platinum 7000 79** **** 6361"
        - "Счет **4305"

    Raises:
        ValueError: Если передан некорректный формат данных.
    """
    if not info or not isinstance(info, str):
        raise ValueError("Некорректный ввод: ожидается не пустая строка")

    # Обработка счета
    if info.startswith("Счет"):
        parts = info.split()
        if len(parts) < 2:
            raise ValueError("Некорректный формат счета")
        account_number = "".join(parts[1:])
        masked = mask_account_number(account_number)
        return f"Счет {masked}"

    # Обработка карты
    match = re.search(r"(\d[\d\s]+\d)$", info)
    if not match:
        raise ValueError("Некорректный формат карты")

    card_number = match.group(1).replace(" ", "")
    card_name = info[: match.start()].strip()
    masked = mask_credit_card(card_number)
    return f"{card_name} {masked}"