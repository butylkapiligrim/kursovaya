import unittest
from typing import Any
from unittest.mock import patch

import pytest

from src.views import create_data_base, five_top_transactions, get_greeting


@pytest.mark.parametrize(
    "hour, expected_result",
    [
        ("06.05.2022 08:00", "Доброе утро"),
        ("06.05.2022 12:00", "Добрый день"),
        ("06.05.2022 18:00", "Добрый вечер"),
        ("06.05.2022 02:00", "Доброй ночи"),
    ],
)
def test_get_greeting(hour: str, expected_result: str) -> None:
    assert get_greeting(hour) == expected_result


@pytest.fixture
def mock_read_files(mocker: Any) -> None:
    mock_transactions = [
        {"Дата операции": "2022-05-06", "Сумма операции": 600, "Категория": "Отели", "Описание": "Airplane ticket"},
        {"Дата операции": "2022-05-05", "Сумма операции": 500, "Категория": "Техника", "Описание": "Home improvement"},
        {"Дата операции": "2022-05-04", "Сумма операции": 400, "Категория": "Аптека", "Описание": "Doctor's visit"},
        {
            "Дата операции": "2022-05-03",
            "Сумма операции": 300,
            "Категория": "Развлечения",
            "Описание": "Movie theater",
        },
        {"Дата операции": "2022-05-02", "Сумма операции": 200, "Категория": "Такси", "Описание": "Gas station"},
    ]
    mocker.patch("your_module.read_files", return_value=mock_transactions)


@pytest.fixture
def mock_get_currency_rate(mocker: Any) -> None:
    mocker.patch(
        "your_module.get_currency_rate",
        side_effect=lambda currency: {
            "USD": 1.05,
            "EUR": 1.10,
        }[currency],
    )


@pytest.fixture
def mock_get_stock_currency(mocker: Any) -> None:
    mocker.patch(
        "src.views.get_stock_currency",
        side_effect=lambda stock: {
            "AAPL": 170.00,
            "AMZN": 3000.00,
            "GOOGL": 2500.00,
            "MSFT": 300.00,
            "TSLA": 1000.00,
        }[stock],
    )


class TestViews(unittest.TestCase):

    @patch("src.views.read")
    def test_five_top_transactions_non_empty(self, mock_read: Any) -> None:
        mock_read.return_value = [
            {"Дата операции": "2023-12-01", "Сумма операции": 100, "Категория": "Food", "Описание": "Магазин"},
            {"Дата операции": "2023-12-02", "Сумма операции": 50, "Категория": "Transport", "Описание": "Проезд"},
            {"Дата операции": "2023-12-03", "Сумма операции": 200, "Категория": "Entertainment", "Описание": "Кино"},
            {"Дата операции": "2023-12-04", "Сумма операции": 150, "Категория": "Food", "Описание": "Ресторан"},
            {"Дата операции": "2023-12-05", "Сумма операции": 75, "Категория": "Shopping", "Описание": "Одежда"},
            {"Дата операции": "2023-12-06", "Сумма операции": 10, "Категория": "Other", "Описание": "Другое"},
        ]
        result = five_top_transactions(mock_read)

        self.assertEqual(result, [])

    @patch("src.views.read")
    @patch("src.views.logger.info")
    @patch("src.views.get_currency_rate")
    @patch("src.views.get_stock_currency")
    def test_create_data_base_no_card(
        self, mock_get_stock_currency: Any, mock_get_currency_rate: Any, mock_logger: Any, mock_read: Any
    ) -> None:
        """Проверяет, что create_data_base обрабатывает случай, когда номер карты не найден."""
        mock_read.return_value = [
            {"Дата операции": "2023-12-01", "Сумма операции": 100, "Категория": "Food", "Описание": "Магазин"},
            {"Дата операции": "2023-12-02", "Сумма операции": 50, "Категория": "Transport", "Описание": "Проезд"},
        ]
        greet = "Доброе утро"
        top_transactions = [{"date": "2023-12-03", "amount": 200, "category": "Entertainment", "description": "Кино"}]
        mock_get_currency_rate.side_effect = lambda currency: 1.0 if currency == "USD" else 0.9
        mock_get_stock_currency.side_effect = lambda stock: 100.0 if stock == "AAPL" else 0.0
        result = create_data_base(greet, top_transactions)
        self.assertEqual(result["greeting"], greet)
        self.assertEqual(result["cards"], [])
        self.assertEqual(result["top_transactions"], top_transactions)
        self.assertEqual(result["currency_rates"], [({"currency": "USD", "rate": 1}, {"currency": "EUR", "rate": 1})])
        self.assertEqual(
            result["stock_prices"],
            [
                [
                    {"stock": "AAPL", "price": 100.0},
                    {"stock": "AMZN", "price": 0.0},
                    {"stock": "GOOGL", "price": 0.0},
                    {"stock": "MSFT", "price": 0.0},
                    {"stock": "TSLA", "price": 0.0},
                ]
            ],
        )

    @patch("src.views.read")
    @patch("src.views.logger.info")
    @patch("src.views.get_currency_rate")
    @patch("src.views.get_stock_currency")
    def test_create_data_base_with_card(
        self, mock_get_stock_currency: Any, mock_get_currency_rate: Any, mock_logger: Any, mock_read: Any
    ) -> None:
        mock_read.return_value = [
            {
                "Дата операции": "2023-12-01",
                "Сумма операции": 100,
                "Категория": "Food",
                "Описание": "Магазин",
                "Номер карты": "1234567890123456",
            },
            {"Дата операции": "2023-12-02", "Сумма операции": 50, "Категория": "Transport", "Описание": "Проезд"},
        ]
        greet = "Добрый день"
        top_transactions = [{"date": "2023-12-03", "amount": 200, "category": "Entertainment", "description": "Кино"}]
        mock_get_currency_rate.side_effect = lambda currency: 1.0 if currency == "USD" else 0.9
        mock_get_stock_currency.side_effect = lambda stock: 100.0 if stock == "AAPL" else 0.0
        result = create_data_base(greet, top_transactions)
        self.assertEqual(result["greeting"], greet)
        self.assertEqual(result["cards"], [{"cashback": 1, "last_digits": "1234567890123456", "total_spent": 100}])
        self.assertEqual(result["top_transactions"], top_transactions)
        self.assertEqual(result["currency_rates"], [({"currency": "USD", "rate": 1}, {"currency": "EUR", "rate": 1})])
        self.assertEqual(
            result["stock_prices"],
            [
                [
                    {"stock": "AAPL", "price": 100.0},
                    {"stock": "AMZN", "price": 0.0},
                    {"stock": "GOOGL", "price": 0.0},
                    {"stock": "MSFT", "price": 0.0},
                    {"stock": "TSLA", "price": 0.0},
                ]
            ],
        )

    @patch("src.views.read")
    @patch("src.views.logger.info")
    @patch("src.views.get_currency_rate")
    @patch("src.views.get_stock_currency")
    def test_create_data_base_duplicate_card(
        self, mock_get_stock_currency: Any, mock_get_currency_rate: Any, mock_logger: Any, mock_read: Any
    ) -> None:
        mock_read.return_value = [
            {
                "Дата операции": "2023-12-01",
                "Сумма операции": 100,
                "Категория": "Food",
                "Описание": "Магазин",
                "Номер карты": "1234567890123456",
            },
            {
                "Дата операции": "2023-12-02",
                "Сумма операции": 50,
                "Категория": "Transport",
                "Описание": "Проезд",
                "Номер карты": "1234567890123456",
            },
        ]
        greet = "Добрый вечер"
        top_transactions = [{"date": "2023-12-03", "amount": 200, "category": "Entertainment", "description": "Кино"}]
        mock_get_currency_rate.side_effect = lambda currency: 1.0 if currency == "USD" else 0.9
        mock_get_stock_currency.side_effect = lambda stock: 100.0 if stock == "AAPL" else 0.0
        result = create_data_base(greet, top_transactions)
        self.assertEqual(result["greeting"], greet)
        self.assertEqual(result["cards"], [{"cashback": 1, "last_digits": "1234567890123456", "total_spent": 100}])
        self.assertEqual(result["top_transactions"], top_transactions)
        self.assertEqual(result["currency_rates"], [({"currency": "USD", "rate": 1}, {"currency": "EUR", "rate": 1})])
        self.assertEqual(
            result["stock_prices"],
            [
                [
                    {"stock": "AAPL", "price": 100.0},
                    {"stock": "AMZN", "price": 0.0},
                    {"stock": "GOOGL", "price": 0.0},
                    {"stock": "MSFT", "price": 0.0},
                    {"stock": "TSLA", "price": 0.0},
                ]
            ],
        )
