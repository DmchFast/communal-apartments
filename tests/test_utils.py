from utils import input_float


def test_input_float_returns_float(monkeypatch) -> None:
    """Проверяет, что input_float возвращает число с плавающей точкой."""
    monkeypatch.setattr("builtins.input", lambda _: "42.5")

    assert input_float("Введите число: ") == 42.5


def test_input_float_retries_on_invalid_input(monkeypatch, capsys) -> None:
    """Проверяет, что при некорректном вводе запрос повторяется."""
    inputs = iter(["abc", "10.5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = input_float("Введите число: ")
    captured = capsys.readouterr()

    assert result == 10.5
    assert "Ошибка: введите число." in captured.out
