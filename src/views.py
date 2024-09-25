import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

from config import VIEWS_LOGS
from src.utils import stock_rates

load_dotenv()
api_key = os.getenv("API_KEY")

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(VIEWS_LOGS, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def calculate_expenses(df: pd.DataFrame, start_date: datetime.date, end_date: datetime.date):

    logger.info("Преобразуем столбец с датой в тип datetime")
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")

    logger.info("Фильтрация по диапазону дат")
    filtered_df = df[(df["Дата платежа"].dt.date >= start_date) & (df["Дата платежа"].dt.date <= end_date)]
    income_filtered = filtered_df[filtered_df["Сумма операции"] > 0]

    logger.info("Считаю сумму расходов")
    total_expenses = filtered_df[filtered_df["Сумма операции"] < 0]["Сумма операции"].sum()
    income_total = income_filtered["Сумма операции"].sum()

    logger.info("Группировка по категориям и вычисление общей суммы по каждой категории")
    grouped = filtered_df.groupby("Категория", as_index=False)["Сумма операции"].sum()
    income_grouped = income_filtered.groupby("Категория", as_index=False)["Сумма операции"].sum()

    logger.info("Сортировка по сумме операций по убыванию")
    sorted_categories = grouped.sort_values(by="Сумма операции", ascending=False)
    income_sorted = income_grouped.sort_values(by="Сумма операции", ascending=False)

    logger.info("Выбор топ-7 категорий")
    top_categories = sorted_categories.head(7)

    logger.info("Остальные категории")
    other_categories = sorted_categories[7:]
    other_total = other_categories["Сумма операции"].sum()

    logger.info('Добавляем категорию "Остальное", если есть остальные категории')
    if not other_categories.empty:
        top_categories = top_categories._append(
            {"Категория": "Остальное", "Сумма операции": other_total}, ignore_index=True
        )

    income_pay = {"total_amount": float(income_total), "main": income_sorted.to_dict(orient="records")}

    logger.info("Фильтрую переводы и наличные")
    transfers_and_cash = df[df["Категория"].isin(["Наличные", "Переводы"])]
    transfers_and_cash_grouped = transfers_and_cash.groupby("Категория", as_index=False)["Сумма операции"].sum()

    logger.info("Апи запрос для получения стоимости иностранных валют")
    payload = {"symbols": "USD,EUR,GBP", "base": "RUB"}
    headers = {"apikey": api_key}

    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.request("GET", url, headers=headers, params=payload, timeout=60)

    status_code = response.status_code

    if status_code == 200:
        exchange_rate = response.json()

    get_sp_500_rate = stock_rates()

    logger.info("Финальный результат")
    result = {
        "expenses": {
            "total_amount": float(total_expenses),
            "main": top_categories.to_dict(orient="records"),
            "transfers_and_cash": transfers_and_cash_grouped.to_dict(orient="records"),
            "income": income_pay,
            "currency_rates": [
                {"currency": "USD", "rate": exchange_rate["rates"]["USD"]},
                {"currency": "EUR", "rate": exchange_rate["rates"]["EUR"]},
                {"currency": "GBP", "rate": exchange_rate["rates"]["GBP"]},
            ],
        },
        "stock_prices": [
            {"stock": get_sp_500_rate[0]["stock"], "price": get_sp_500_rate[0]["price"]},
            {"stock": get_sp_500_rate[1]["stock"], "price": get_sp_500_rate[1]["price"]},
            {"stock": get_sp_500_rate[2]["stock"], "price": get_sp_500_rate[2]["price"]},
            {"stock": get_sp_500_rate[3]["stock"], "price": get_sp_500_rate[3]["price"]},
            {"stock": get_sp_500_rate[4]["stock"], "price": get_sp_500_rate[4]["price"]},
        ],
    }

    return json.dumps(result, ensure_ascii=False)
