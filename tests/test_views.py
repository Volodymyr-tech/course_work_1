import datetime
import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import calculate_expenses


# Параметризация для различных входных данных
@pytest.mark.parametrize(
    "df, start_date, end_date, expected_total",
    [
        (
            pd.DataFrame(
                {
                    "Дата платежа": ["01.01.2022", "05.01.2022", "10.01.2022"],
                    "Сумма операции": [-100, 200, -300],
                    "Категория": ["Продукты", "Зарплата", "Одежда"],
                }
            ),
            datetime.date(2022, 1, 1),
            datetime.date(2022, 1, 31),
            -400,
        ),
        (
            pd.DataFrame(
                {
                    "Дата платежа": ["01.02.2022", "05.02.2022", "10.02.2022"],
                    "Сумма операции": [-50, -200, 300],
                    "Категория": ["Наличные", "Фастфуд", "Переводы"],
                }
            ),
            datetime.date(2022, 2, 1),
            datetime.date(2022, 2, 28),
            -250,
        ),
    ],
)
@patch("requests.get")
@patch("src.views.stock_rates")  # Мокаем вызов stock_rates
def test_calculate_expenses(mock_stock_rates, mock_get, df, start_date, end_date, expected_total):
    # Мокаем ответ для API валютных курсов
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"USD": 74.0, "EUR": 85.0, "GBP": 100.0}}

    # Мокаем ответ для stock_rates
    mock_stock_rates.return_value = mock_stock_rates.return_value = [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "TSLA", "price": 1007.08},
    ]

    # Вызов тестируемой функции
    result = calculate_expenses(df, start_date, end_date)

    # Проверка, что общая сумма расходов верна
    assert json.loads(result)["expenses"]["total_amount"] == expected_total
    assert "currency_rates" in json.loads(result)["expenses"]
    assert "stock_prices" in json.loads(result)
