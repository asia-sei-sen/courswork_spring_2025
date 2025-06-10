from views import main_page_view
import json


def test_main_page_view():
    input_date = "2025-06-07 09:30:00"
    result_json = main_page_view(input_date)
    assert isinstance(result_json, str)

    result = json.loads(result_json)
    assert "greeting" in result
    assert "cards" in result
    assert isinstance(result["greeting"], str)
    assert len(result["cards"]) > 0
