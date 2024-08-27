import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.logger import loggingg

logger = loggingg()


def read(file_path: Any) -> Any:
    """Открытие файлов расширений: '.xlsx' или '.json'"""
    file_extension = Path(file_path).suffix.lower()

    if file_extension == ".xlsx":
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    elif file_extension == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("Неподдерживаемый формат файла")


def writes(files: Any, results: Any) -> None:
    """
    Функция, которая записывает результаты в указанный файл.
    """
    if files.endswith(".txt"):
        with open(files, "a") as files:
            files.write(results)
    elif files.endswith(".json"):
        with open(files, "w", encoding="utf8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
