import pandas as pd
import os
import datetime
from src.xlsx_reader import pandas_reader_xlsx
import requests
from dotenv import load_dotenv
from src.utils import get_date_range

load_dotenv()
api_key = os.getenv("API_KEY")

def calculate_expenses(df: pd.DataFrame, start_date: datetime.date, end_date: datetime.date):
    # Преобразуем столбец с датой в тип datetime
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")

    # Фильтрация по диапазону дат
    filtered_df = df[(df["Дата платежа"].dt.date >= start_date) & (df["Дата платежа"].dt.date <= end_date)]
    income_filtered = filtered_df[filtered_df["Сумма операции"] > 0]

    # Сумма расходов
    total_expenses = filtered_df["Сумма операции"].sum()
    income_total = income_filtered["Сумма операции"].sum()

    # Группировка по категориям и вычисление общей суммы по каждой категории
    grouped = filtered_df.groupby("Категория", as_index=False)["Сумма операции"].sum()
    income_grouped = income_filtered.groupby("Категория", as_index=False)["Сумма операции"].sum()

    # Сортировка по сумме операций по убыванию
    sorted_categories = grouped.sort_values(by="Сумма операции", ascending=False)
    income_sorted = income_grouped.sort_values(by="Сумма операции", ascending=False)

    # Выбор топ-7 категорий
    top_categories = sorted_categories.head(7)

    # Остальные категории
    other_categories = sorted_categories[7:]
    other_total = other_categories["Сумма операции"].sum()

    # Добавляем категорию "Остальное", если есть остальные категории
    if not other_categories.empty:
        top_categories = top_categories._append(
            {"Категория": "Остальное", "Сумма операции": other_total}, ignore_index=True
        )

    income_pay = {"total_amount": float(income_total), "main": income_sorted.to_dict(orient="records")}

    # Переводы и наличные
    transfers_and_cash = df[df["Категория"].isin(["Наличные", "Переводы"])]
    transfers_and_cash_grouped = transfers_and_cash.groupby("Категория", as_index=False)["Сумма операции"].sum()

    # Апи запрос для получения стоимости иностранных валют
    payload = {"symbols": "USD,EUR,GBP", "base": "RUB"}
    headers = {"apikey": api_key}

    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.request("GET", url, headers=headers, params=payload, timeout=60)

    status_code = response.status_code

    if status_code == 200:
        exchange_rate = response.json()


    # Финальный результат
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
        }
    }

    return result


if __name__ == "__main__":
    path = r"C:\Users\Владимир\PycharmProjects\pythonProject1\data\operations.xlsx"

    # Загрузка данных через Pandas
    data_fraime = pandas_reader_xlsx(path)

    # Получаем дату начала и конца для фильтрации
    start_date, end_date = get_date_range("05.11.2021", "M")

    # Вычисляем расходы
    res = calculate_expenses(data_fraime, start_date, end_date)
    print(res)