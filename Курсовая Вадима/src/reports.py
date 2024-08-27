from datetime import datetime, timedelta
from typing import Any, Optional

import pandas as pd

from src.logger import loggingg
from src.utils import writes

logger = loggingg()


def save_report_to_file(func: Any) -> Any:
    def wrapper(transactions: pd.DataFrame, category: str, date: Optional[pd.Timestamp] = None) -> Any:
        try:
            final = func(transactions, category, date)
            writes("reports.json", final)
            return final
        except Exception:
            return None

    return wrapper


@save_report_to_file
def expenses_by_category(transactions: pd.DataFrame, category: str, date_base: Optional[pd.Timestamp] = None) -> Any:
    """
    Функция, которая принимает на вход список транзакций и возвращает словарь с расходами по указанной категории.
    """
    date_base = pd.to_datetime(date_base) if date_base else pd.to_datetime("today")
    three_months_ago = date_base - timedelta(days=90)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    filter_of_transactions = transactions[
        (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= date_base)
        & (transactions["Категория"] == category)
    ]
    all = -filter_of_transactions["Сумма операции"].sum()
    final = {"amount": filter_of_transactions["Сумма операции"].to_dict(), "category": category, "all": all}
    logger.info(f"Расходы по категории '{category}': {final}")
    return final


def reports() -> None:
    print(f'Reports: \n{expenses_by_category("../data/operations.xlsx", "Фастфуд", datetime(2022, 4, 10))}')
