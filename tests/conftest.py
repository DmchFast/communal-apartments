import pytest


@pytest.fixture
def empty_meters() -> list:
    """Пустой список счётчиков."""
    return []


@pytest.fixture
def empty_readings() -> list:
    """Пустой список показаний."""
    return []
