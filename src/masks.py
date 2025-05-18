from decorators.log import (
    log,
)


@log(filename="masks.log")
def mask_credit_card(card_number: str) -> str:
    card_number = card_number.replace(" ", "")
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Некорректный номер карты")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


@log(filename="masks.log")
def mask_account_number(account_number: str) -> str:
    account_number = account_number.replace(" ", "")
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Некорректный номер счета")
    return f"**{account_number[-4:]}"
