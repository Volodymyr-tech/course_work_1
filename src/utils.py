import json
import os
import datetime

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

def reader_json(path: str) -> dict:
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    data = reader_json("../data/operations.json")
    print(data)
