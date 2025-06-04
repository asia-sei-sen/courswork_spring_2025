from datetime import (
    datetime,
)
from typing import (
    Dict,
    List,
    Optional,
)
from collections import (
    Counter,
)
import re

from decorators.log import (
    log,
)


@log(filename="processing.log")
def filter_by_state(transactions: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """Фильтрует транзакции по указанному статусу."""
    return [t for t in transactions if t.get('state') == state]


@log(filename="processing.log")
def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """Сортирует транзакции по дате (по умолчанию - по убыванию)."""
    def get_date(transaction: Dict) -> datetime:
        date_str = transaction.get('date')
        if not isinstance(date_str, str):
            return datetime.min
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            return datetime.min

    return sorted(transactions, key=get_date, reverse=reverse)


@log(filename="processing.log")
def filter_by_description(transactions: List[Dict], search_str: str) -> List[Dict]:
    """
    Фильтрует транзакции по наличию строки в описании.
    Поиск регистронезависимый, использует регулярные выражения.
    """
    pattern = re.compile(re.escape(search_str), re.IGNORECASE)
    return [t for t in transactions if 'description' in t and pattern.search(t['description'])]


@log(filename="processing.log")
def count_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по указанным категориям.
    Категории ищутся в поле description.
    """
    cnt = Counter()
    for t in transactions:
        desc = t.get('description', '').lower()
        for cat in categories:
            if cat.lower() in desc:
                cnt[cat] += 1
    return dict(cnt)