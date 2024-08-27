import json
import os
from datetime import datetime
from typing import Any

import requests
import yfinance as yf
from dotenv import load_dotenv

from src.logger import loggingg
from src.utils import read, writes

load_dotenv()
api_key = os.getenv("API_KEY")
logger = loggingg()


def get_greeting(hour: Any) -> str:
    """
    Возвращает приветственное сообщение в зависимости от времени суток.
    """
    if hour is None:
        hour = datetime.now()
    else:
        hour = datetime.strptime(hour, "%d.%m.%Y %H:%M")
    hour = hour.hour
    if 5 < hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def five_top_transactions(reader: Any) -> list[dict[str, Any]] | None:
    """
    Возвращает топ-5 транзакций пользователя по сумме.
    """
    if reader is not None:
        return [
            {
                "date": transaction["Дата операции"],
                "amount": round(transaction["Сумма операции"]),
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
            for transaction in sorted(reader, key=lambda item: item["Сумма операции"], reverse=True)[:5]
        ]
    else:
        return None


def get_currency_rate(currency: Any) -> Any:
    """
    Возвращает курс валюты.
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": api_key}, timeout=15)
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    return rate


def get_stock_currency(stock: str) -> Any:
    """
    Возвращает курс акции.
    """
    ticker = yf.Ticker(stock)
    todays_data = ticker.history(period="1d")

    if not todays_data.empty:
        high_price = todays_data["High"].iloc[0]
        return high_price
    else:
        return 0.0


def create_data_base(greet: Any, top_5_transactions: Any) -> Any:
    """
    Возвращает словарь с данными пользователя.
    """
    data = {"greeting": greet, "cards": [], "top_transactions": [], "currency_rates": [], "stock_prices": []}
    if read("../data/operations.xlsx"):
        logger.info("Файл был прочитан.")

        card_number = None
        total_sum = 0
        cash = 0

        for transaction in read("../data/operations.xlsx"):
            card_number = transaction.get("Номер карты")
            if card_number is not None:
                logger.info(f"Найден номер карты: {card_number}")
                total_sum += transaction.get("Сумма операции", 0)
                cash = total_sum // 100
                break

        if card_number is not None:
            if card_number not in [card["last_digits"] for card in data["cards"]]:
                data["cards"].append(
                    {"last_digits": card_number, "total_spent": round(total_sum, 2), "cashback": cash}
                )
                logger.info(f"Номер карты: {card_number} добавлен в базу данных.")

        data["top_transactions"] = top_5_transactions
        data["currency_rates"].append(
            (
                {"currency": "USD", "rate": round(get_currency_rate("USD"))},
                {"currency": "EUR", "rate": round(get_currency_rate("EUR"))},
            )
        )
        data["stock_prices"].append(
            [
                {"stock": "AAPL", "price": round(get_stock_currency("AAPL"), 2)},
                {"stock": "AMZN", "price": round(get_stock_currency("AMZN"), 2)},
                {"stock": "GOOGL", "price": round(get_stock_currency("GOOGL"), 2)},
                {"stock": "MSFT", "price": round(get_stock_currency("MSFT"), 2)},
                {"stock": "TSLA", "price": round(get_stock_currency("TSLA"), 2)},
            ]
        )

        logger.info("добавление операций в базу данных.")

    return data


def views() -> None:
    time = input("Введите время в формате - DD.MM.YYYY HH:MM):")
    greeting = get_greeting(time if time else None)
    transactions = five_top_transactions(read("../data/operations.xlsx"))
    result = create_data_base(greeting, transactions)
    writes("views.json", result)
    print(f"Views: {result}")
