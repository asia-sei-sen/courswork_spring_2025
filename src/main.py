import os
from src.file_parsers.csv_parser import read_csv
from src.file_parsers.excel_parser import read_excel
from src.utils import load_json_file
from src.processing import (
    filter_by_state,
    sort_by_date,
    filter_by_description,
    count_by_category
)
from src.external_api import convert_to_rub
from src.widget import get_date, mask_account_card

DATA_DIR = "./data"
FILENAME = "transactions.json"  # или "transactions.csv", "transactions.xlsx"

def main():
    # 1. Загрузка данных
    file_path = os.path.join(DATA_DIR, FILENAME)
    if FILENAME.endswith(".json"):
        transactions = load_json_file(file_path)
    elif FILENAME.endswith(".csv"):
        transactions = read_csv(file_path)
    elif FILENAME.endswith(".xlsx"):
        transactions = read_excel(file_path)
    else:
        raise ValueError("Неподдерживаемый формат файла")

    print(f"Загружено транзакций: {len(transactions)}")

    # 2. Фильтрация и сортировка
    executed = filter_by_state(transactions)
    sorted_tx = sort_by_date(executed)

    # 3. Поиск по описанию
    keyword = "оплата"
    filtered = filter_by_description(sorted_tx, keyword)

    # 4. Подсчет категорий
    category_counts = count_by_category(filtered, ["магазин", "услуга", "перевод"])
    print("Категории:", category_counts)

    # 5. Вывод информации по первым 5 транзакциям
    print("\nПримеры транзакций:")
    for tx in filtered[:5]:
        date = get_date(tx.get("date"))
        description = tx.get("description", "—")
        from_ = mask_account_card(tx.get("from", ""))
        to_ = mask_account_card(tx.get("to", ""))
        amount_rub = convert_to_rub({
            "amount": tx.get("operationAmount", {}).get("amount", 0),
            "currency": tx.get("operationAmount", {}).get("currency", {}).get("code", "RUB")
        })

        print(f"{date} | {description}")
        print(f"{from_} → {to_}")
        print(f"{amount_rub:.2f} RUB")
        print("-" * 40)

if __name__ == "__main__":
    main()
