from config import UTILS_LOGS
import os
import datetime
import logging
from dotenv import load_dotenv
import requests
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(UTILS_LOGS, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


load_dotenv()


def start_of_week(date: datetime.date) -> datetime.date:
    # Функция для получения начала недели
    start = date - datetime.timedelta(days=date.weekday())
    return start


def start_of_month(date: datetime.date) -> datetime.date:
    # Функция для получения начала месяца
    start = date.replace(day=1)
    return start


def start_of_year(date: datetime.date) -> datetime.date:
    # Функция для получения начала года
    start = date.replace(month=1, day=1)
    return start


def get_date_range(date_str: str, range_type: str = "M") -> (datetime.date, datetime.date):
    # Преобразуем строку с датой в объект datetime
    date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

    if range_type == "W":  # Неделя
        start_date = start_of_week(date)
    elif range_type == "M":  # Месяц
        start_date = start_of_month(date)
    elif range_type == "Y":  # Год
        start_date = start_of_year(date)
    elif range_type == "ALL":  # Все данные до даты
        start_date = datetime.date.min
    else:
        raise ValueError(f"Неподдерживаемый диапазон: {range_type}")

    return start_date, date


def stock_rates(users_stocks: List[str] = ["AAPL", "AMZN", "GOOGL", "NVDA", "META"]) -> List[Dict[str, Any]]:
    """Функция принимает список акций. Возвращает котировки, полученные через API."""
    logger.info("Функция начала свою работу.")
    try:
        result_stocks_list = []
        load_dotenv()
        api_key = os.getenv("API_ALPHA")
        logger.info("Функция получает данные по котировкам.")
        for stock in users_stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = requests.get(url, timeout=5, allow_redirects=False)
            result = response.json()
            logger.info(f"{result}")
            result_stocks_list.append({"stock": stock, "price": round(float(result["Global Quote"]["05. price"]), 2)})
        logger.info("Функция успешно завершила свою работу.")
        return result_stocks_list
    except Exception:
        logger.error("При работе функции произошла ошибка!")
        raise Exception("При работе функции произошла ошибка!")


if __name__ == "__main__":
    res = stock_rates()
    print(res)
