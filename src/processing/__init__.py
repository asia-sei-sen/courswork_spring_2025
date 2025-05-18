from datetime import (
    datetime,
)
from typing import (
    Dict,
    List,
)

from decorators.log import (
    log,
)


@log(filename="processing.log")
def filter_by_state(transactions: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    return [t for t in transactions if t.get('state') == state]

@log(filename="processing.log")
def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    def get_date(transaction: Dict) -> datetime:
        date_str = transaction.get('date')
        if not isinstance(date_str, str):
            return datetime.min
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            return datetime.min

    return sorted(transactions, key=get_date, reverse=reverse)
