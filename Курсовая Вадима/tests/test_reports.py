import logging
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.reports import expenses_by_category

logging.basicConfig(level=logging.INFO)


@patch("src.services.logger")
def test_expenses_by_category_with_date(mock_logger: Any) -> None:
    """Проверяет, что функция expenses_by_category работает корректно с датой."""
    transactions = pd.DataFrame(
        {
            "Дата операции": ["2023-10-25", "2023-10-26", "2023-11-01"],
            "Сумма операции": [10, 20, 30],
            "Категория": ["Food", "Food", "Entertainment"],
        }
    )

    result = expenses_by_category(transactions, "Food", pd.to_datetime("2023-11-01"))
    assert result == None


@patch("src.services.logger")
def test_expenses_by_category_without_date(mock_logger: Any) -> None:
    transactions = pd.DataFrame(
        {
            "Дата операции": ["2023-10-25", "2023-10-26", "2023-11-01"],
            "Сумма операции": [10, 20, 30],
            "Категория": ["Food", "Food", "Entertainment"],
        }
    )

    result = expenses_by_category(transactions, "Food")
    assert result == None


@patch("src.services.logger")
def test_expenses_by_category_empty_category(mock_logger: Any) -> None:
    """Проверяет, что функция expenses_by_category возвращает пустой словарь для пустой категории."""
    transactions = pd.DataFrame(
        {
            "Дата операции": ["2023-10-25", "2023-10-26", "2023-11-01"],
            "Сумма операции": [10, 20, 30],
            "Категория": ["Food", "Food", "Entertainment"],
        }
    )
    result = expenses_by_category(transactions, "NonexistentCategory")
    assert result == None


@patch("src.services.logger")
def test_expenses_by_category_invalid_date(mock_logger: Any) -> None:
    """Проверяет, что функция expenses_by_category работает корректно с некорректной датой."""
    transactions = pd.DataFrame(
        {
            "Дата операции": ["2023-10-25", "2023-10-26", "2023-11-01"],
            "Сумма операции": [10, 20, 30],
            "Категория": ["Food", "Food", "Entertainment"],
        }
    )

    result = expenses_by_category(transactions, "Food", "invalid_date")
    assert result == None
