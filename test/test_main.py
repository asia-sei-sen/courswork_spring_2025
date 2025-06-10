import builtins

import pytest

from src import main


def test_main_function_exists():
    assert callable(main.main)


@pytest.mark.parametrize(
    "inputs",
    [
        ("4\n"),  # Неверный выбор — проверка выхода из main
    ],
)
def test_main_invalid_choice(monkeypatch, capsys, inputs):
    monkeypatch.setattr(builtins, "input", lambda _: inputs.strip())
    main.main()
    captured = capsys.readouterr()
    assert "Неверный выбор" in captured.out
