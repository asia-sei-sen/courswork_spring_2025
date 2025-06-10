import logging
from datetime import datetime

from invest_savings import run_invest_savings
from views import main_page_view
from reports import spending_by_weekday
import pandas as pd


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    print("Выберите модуль:")
    print("1 - Инвесткопилка")
    print("2 - Главная страница")
    print("3 - Отчёт: Траты по категории")

    choice = input("Ваш выбор (1/2/3): ").strip()

    if choice == "1":
        file_path = input("Введите путь к файлу Excel с транзакциями: ")
        month = input("Введите месяц в формате YYYY-MM (например, 2025-03): ")
        round_limit = int(input("Введите округление (например, 100): "))
        result = run_invest_savings(file_path, month, round_limit)
        print(result)

    elif choice == "2":
        input_datetime = input("Введите дату и время (YYYY-MM-DD HH:MM:SS): ")
        result = main_page_view(input_datetime)
        print(result)

    elif choice == "3":
        file_path = input("Введите путь к файлу Excel с транзакциями: ")
        category = input("Введите категорию (например, 'еда'): ")
        date_input = input("Введите дату отсчёта (YYYY-MM-DD) или оставьте пустым для текущей: ").strip()

        df = pd.read_excel(file_path, engine="openpyxl")
        start_date = datetime.strptime(date_input, "%Y-%m-%d") if date_input else None
        result = spending_by_weekday(df, category, start_date)
        print(result)

    else:
        print("Неверный выбор.")


if __name__ == "__main__":
    main()
