import json
from pathlib import Path
from typing import Any


def load_json(filename: str) -> Any:
    #Загрузка данные из JSON-файла
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_json(filename: str, data: Any) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)