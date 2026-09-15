import pytest


@pytest.fixture
def empty_meters() -> dict:
    """Пустой словарь счётчиков."""
    return {}


@pytest.fixture
def empty_readings() -> list:
    """Пустой список показаний."""
    return []