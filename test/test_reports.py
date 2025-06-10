import pandas as pd
from src.reports import spending_by_weekday
import json


def test_spending_by_weekday_returns_correct_json():
    data = {
        "date": ["2025-03-01", "2025-03-02", "2025-03-03", "2025-05-30", "2025-05-31"],
        "category": ["еда", "еда", "транспорт", "еда", "еда"],
        "amount": [100, 200, 300, 400, 500],
    }
    df = pd.DataFrame(data)

    # Входные параметры
    category = "еда"
    start_date = "2025-05-31"  # конец периода

    result_json = spending_by_weekday(df, category, start_date)

    # Парсим результат обратно в dict
    result = json.loads(result_json)

    # Проверяем ключи — все дни недели должны быть
    expected_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    assert set(result.keys()) == set(expected_days)

    # Проверяем, что средние траты на понедельник (2025-03-31 — это понедельник? Проверим)
    # Для 2025-05-31 — суббота, период 90 дней назад — 2025-03-02
    # Данные по еде попадают: 2025-03-02 (воскресенье), 2025-05-30 (пятница), 2025-05-31 (суббота)
    # Средние по этим дням:
    # Воскресенье (Sunday) — 200
    # Пятница (Friday) — 400
    # Суббота (Saturday) — 500
    # Остальные — 0

    assert abs(result["Sunday"] - 200) < 0.01
    assert abs(result["Friday"] - 400) < 0.01
    assert abs(result["Saturday"] - 500) < 0.01

    # Остальные дни недели должны быть 0
    for day in expected_days:
        if day not in ["Sunday", "Friday", "Saturday"]:
            assert result[day] == 0


def test_spending_by_weekday_no_data():
    df = pd.DataFrame({"date": [], "category": [], "amount": []})

    category = "еда"
    start_date = "2025-06-01"

    result_json = spending_by_weekday(df, category, start_date)
    result = json.loads(result_json)

    assert "message" in result
    assert result["message"] == "Нет данных для выбранного периода и категории"
