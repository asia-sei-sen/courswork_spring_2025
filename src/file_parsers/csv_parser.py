import csv
from typing import List, Dict


def read_csv(file_path: str) -> List[Dict]:
    """
    Читает CSV-файл с финансовыми транзакциями и возвращает список словарей.

    :param file_path: Путь к CSV-файлу.
    :return: Список транзакций в виде словарей.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))