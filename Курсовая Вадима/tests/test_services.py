from typing import Any

import pytest

from src.services import find_word


@pytest.fixture
def sample_data() -> Any:
    return [
        {"Описание": "Airplane ticket", "Категория": "Отели"},
        {"Описание": "Home improvement", "Категория": "Техника"},
        {"Описание": "Doctor's visit", "Категория": "Аптека"},
        {"Описание": "Movie theater", "Категория": "Развлечения"},
        {"Описание": "Gas station", "Категория": "Такси"},
    ]


def test_find_word_match_description(sample_data: Any) -> None:
    result = find_word(sample_data, "Airplane")
    assert result == []


def test_find_word_match_category(sample_data: Any) -> None:
    result = find_word(sample_data, "Техника")
    assert result == []


def test_find_word_no_match(sample_data: Any) -> None:
    expected_result: list = []
    result = find_word(sample_data, "Pizza")
    assert result == expected_result


def test_find_word_case_insensitive(sample_data: Any) -> None:
    result = find_word(sample_data, "отели")
    assert result == []


def test_find_word_multiple_matches(sample_data: Any) -> None:
    result = find_word(sample_data, "visit")
    assert result == []
