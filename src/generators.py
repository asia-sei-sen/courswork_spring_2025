from decorators.log import (
    log,
)


@log(filename="generator.log")
def filter_by_currency(transactions: list[dict], currency: str) -> iter:
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction

@log(filename="generator.log")
def transaction_descriptions(transactions: list[dict]) -> iter:
    for transaction in transactions:
        yield transaction["description"]

@log(filename="generator.log")
def card_number_generator(start: int, end: int) -> iter:
    for number in range(start, end + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[8:12] + " " + f"{number:016d}"[12:16]
