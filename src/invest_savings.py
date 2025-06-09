import pandas as pd
import json
from datetime import datetime

def read_transactions_from_excel(path):
    try:
        df = pd.read_excel(path, engine='openpyxl')
        if not {"date", "amount"}.issubset(df.columns):
            return []
        transactions = df[["date", "amount"]].to_dict(orient="records")
        # Можно дополнительно преобразовать даты к строкам, если нужно
        for t in transactions:
            if isinstance(t["date"], pd.Timestamp):
                t["date"] = t["date"].strftime("%Y-%m-%d")
        return transactions
    except Exception:
        return []

def investkopilka(month, transactions, round_limit):
    try:
        total_round_up = 0.0
        for t in transactions:
            # Проверяем дату на соответствие месяцу
            if t.get("date", "").startswith(month):
                amount = float(t.get("amount", 0))
                round_up = round_limit - (amount % round_limit) if amount % round_limit != 0 else 0
                total_round_up += round_up
        result = {
            "month": month,
            "round_limit": round_limit,
            "total_round_up": round(total_round_up, 2)
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

def run_invest_savings(filepath, month, round_limit):
    transactions = read_transactions_from_excel(filepath)
    if not transactions:
        return json.dumps([])
    return investkopilka(month, transactions, round_limit)
