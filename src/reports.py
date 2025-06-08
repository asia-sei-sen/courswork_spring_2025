import json
import logging
from datetime import datetime, timedelta
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def spending_by_weekday(df: pd.DataFrame, category: str, start_date: str = None) -> str:
    """
    Отчёт: средние траты по дням недели за последние 3 месяца от start_date (или текущей даты).
    df должен содержать колонки: 'date', 'category', 'amount'.
    Возвращает JSON со средней суммой трат по каждому дню недели.
    """
    try:
        if start_date:
            current_date = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            current_date = datetime.now()

        period_start = current_date - timedelta(days=90)  # последние 3 месяца

        logger.info(f"Формируем отчет по категории '{category}' за период {period_start.date()} - {current_date.date()}")

        # Фильтрация по дате и категории
        df['date'] = pd.to_datetime(df['date'])
        filtered = df[
            (df['date'] >= period_start) &
            (df['date'] <= current_date) &
            (df['category'] == category)
        ]

        if filtered.empty:
            logger.warning("Нет данных для выбранного периода и категории")
            return json.dumps({"message": "Нет данных для выбранного периода и категории"}, ensure_ascii=False)

        # Группируем по дню недели (понедельник=0) и считаем средние траты
        grouped = filtered.groupby(filtered['date'].dt.day_name())['amount'].mean()

        # Чтобы дни недели шли в естественном порядке (Пн, Вт, Ср, ...)
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        grouped = grouped.reindex(days_order).fillna(0).round(2)

        # Формируем словарь
        result = {day: grouped[day] for day in days_order}

        logger.info("Отчет успешно сформирован")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка формирования отчёта: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)
