import os
from invest_savings import read_transactions_from_excel

def test_read_transactions(tmp_path):
    # Создаем небольшой Excel файл с нужными данными в папке tmp_path
    import pandas as pd

    data = {
        "date": ["2025-05-01", "2025-05-15"],
        "amount": [100.0, 150.5]
    }
    df = pd.DataFrame(data)
    test_file = tmp_path / "test_operations.xlsx"
    df.to_excel(test_file, index=False)

    # Вызов функции чтения
    transactions = read_transactions_from_excel(str(test_file))

    # Проверяем, что список не пустой
    assert isinstance(transactions, list)
    assert len(transactions) == 2

    # Проверяем, что в первом элементе есть ключи
    assert "date" in transactions[0]
    assert "amount" in transactions[0]

