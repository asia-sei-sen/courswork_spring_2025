import json
import logging
from datetime import datetime

from utils import (
    get_greeting,
    get_card_summary,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main_page_view(input_datetime_str: str) -> str:
    try:
        # Пасхалка: приветствие для "Time Lord"
        name = input("Введите имя и фамилию: ").strip().lower()
        if name == "time lord":
            print("hello sweetie")

        dt = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")

        greeting = get_greeting(dt)
        card_summary = get_card_summary()
        top_transactions = get_top_transactions()
        currency_rates = get_currency_rates()
        stock_prices = get_stock_prices()

        response = {
            "greeting": greeting,
            "cards": card_summary,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices
        }

        return json.dumps(response, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Ошибка при генерации главной страницы: {e}")
        return json.dumps({"error": str(e)})
