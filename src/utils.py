import json
import logging
from datetime import datetime, time

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_greeting(dt: datetime) -> str:
    current_time = dt.time()
    if time(5, 0) <= current_time < time(12, 0):
        return "Доброе утро"
    elif time(12, 0) <= current_time < time(18, 0):
        return "Добрый день"
    elif time(18, 0) <= current_time < time(23, 0):
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_summary(transactions: list[dict]) -> list[dict]:
    df = pd.DataFrame(transactions)
    if "card_number" not in df.columns or "amount" not in df.columns:
        logger.error("В данных нет нужных колонок: 'card_number' и 'amount'")
        return []
    df["card_last4"] = df["card_number"].astype(str).str[-4:]
    df_expenses = df[df["amount"] < 0]
    grouped = df_expenses.groupby("card_last4")["amount"].sum().reset_index()
    result = []
    for _, row in grouped.iterrows():
        total_spent = abs(row["amount"])
        cashback = int(total_spent // 100)
        result.append({"card_last4": row["card_last4"], "total_spent": round(total_spent, 2), "cashback": cashback})
    return result


def get_top_transactions(transactions: list[dict], top_n=5) -> list[dict]:
    df = pd.DataFrame(transactions)
    if "amount" not in df.columns:
        logger.error("В данных нет колонки 'amount'")
        return []
    df["abs_amount"] = df["amount"].abs()
    top_df = df.nlargest(top_n, "abs_amount")
    fields = ["date", "amount", "description"] if "description" in df.columns else ["date", "amount"]
    result = top_df[fields].to_dict(orient="records")
    return result


def get_currency_rates() -> dict:
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = {
            "USD": data["Valute"]["USD"]["Value"],
            "EUR": data["Valute"]["EUR"]["Value"],
            "CNY": data["Valute"]["CNY"]["Value"],
        }
        return rates
    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return {}


def get_stock_prices() -> dict:
    prices = {
        "AAPL": 170.33,
        "MSFT": 320.45,
        "GOOGL": 126.54,
        "AMZN": 140.21,
        "TSLA": 750.12,
    }
    return prices


def prepare_main_page_response(dt_str: str, transactions: list[dict]) -> str:
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error(f"Неверный формат даты: {e}")
        dt = datetime.now()
    greeting = get_greeting(dt)
    cards = get_card_summary(transactions)
    top_transactions = get_top_transactions(transactions)
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    return json.dumps(response, ensure_ascii=False, indent=2)
