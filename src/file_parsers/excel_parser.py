import pandas as pd
from typing import List, Dict


def read_excel(file_path: str) -> List[Dict]:
    """
    Читает Excel-файл с финансовыми транзакциями и возвращает список словарей.

    :param file_path: Путь к Excel-файлу (.xlsx).
    :return: Список транзакций в виде словарей.
    """
    df = pd.read_excel(file_path)
    return df.to_dict(orient='records')