import json
import logging
from datetime import datetime
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_transactions_from_excel(file_path: str):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        # Проверяем, что в файле есть необходимые колонки
        required_cols = {'date', 'amount'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise ValueError(f"В файле отсутствуют колонки: {missing}")
        transactions = df.to_dict(orient='records')
        logger.info(f"Прочитано транзакций: {len(transactions)}")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка чтения файла Excel: {e}")
        return []

def investkopilka(month: str, transactions: list, round_limit: int):
    logger.info(f"Start investkopilka for month: {month}, round_limit: {round_limit}")
    try:
        filtered = [
            t for t in transactions
            if datetime.strptime(str(t["date"]), "%Y-%m-%d").strftime("%Y-%m") == month
        ]
        logger.info(f"Filtered transactions count: {len(filtered)}")

        total_round = 0
        for t in filtered:
            amount = float(t["amount"])
            remainder = round_limit - (int(amount) % round_limit)
            if remainder != round_limit:
                total_round += remainder

        result = {
            "month": month,
            "round_limit": round_limit,
            "total_round_up": total_round
        }
        logger.info("Investkopilka calculation finished")
        return json.dumps(result)

    except Exception as e:
        logger.error(f"Error in investkopilka: {e}")
        return json.dumps({"error": str(e)})
