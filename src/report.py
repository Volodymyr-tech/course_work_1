import datetime
from typing import Optional
import pandas as pd
from dateutil.relativedelta import relativedelta
from src.xlsx_reader import pandas_reader_xlsx
import json
from config import REPORTS_LOGS, LOGS_DIR
import os
import logging
from functools import wraps

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(REPORTS_LOGS, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def save_report_to_file(filename: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("Выполняем функцию декоратор и получаем результат")
            result = func(*args, **kwargs)

            logger.info("Устанавливаем имя файла")
            if filename:
                file_name = filename
            else:
                logger.info("Имя по умолчанию: report_<текущая дата и время>.json")
                current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_name = f"report_{current_time}.json"

            report_path = os.path.join(LOGS_DIR, file_name)
            logger.info("Записываем результат в файл")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(result)

            return result

        return wrapper

    return decorator


@save_report_to_file()
def spending_by_workday(transactions: pd.DataFrame, date_: Optional[str] = None) -> pd.DataFrame:

    if date_ is None:
        logger.info("Установка даты по умолчанию")
        date_ = datetime.datetime.now().date()
        logger.info("Отнимаем 3 месяца от даты.")
        start_date = date_ - relativedelta(months=3)

    elif isinstance(date_, str):
        logger.info("Проверка даты переданную в функцию")
        date_ = datetime.datetime.strptime(date_, "%d.%m.%Y").date()
        logger.info("Отнимаем 3 месяца от даты.")
        start_date = date_ - relativedelta(months=3)

    logger.info("Убираем пустые строки без даты")
    transactions_filtered = transactions[
        transactions["Дата платежа"].notnull() & (transactions["Сумма операции"] < 0)
    ].copy()

    logger.info("Преобразуем столбец с датами в datetime")
    transactions_filtered["Дата платежа"] = pd.to_datetime(transactions_filtered["Дата платежа"], dayfirst=True)

    logger.info("Фильтр данных по диапазону в 3 месяца")
    filtered_df = transactions_filtered[
        (transactions_filtered["Дата платежа"].dt.date >= start_date)
        & (transactions_filtered["Дата платежа"].dt.date <= date_)
    ]

    work_day_data = filtered_df[filtered_df["Дата платежа"].dt.weekday < 5]
    work_day = work_day_data["Сумма операции"].mean() if not work_day_data.empty else 0

    day_off_data = filtered_df[filtered_df["Дата платежа"].dt.weekday >= 5]
    day_off = day_off_data["Сумма операции"].mean() if not day_off_data.empty else 0

    data_to_json = {
        "Средняя трата в рабочий день": round(work_day, 2),
        "Средняя трата в выходной день": round(day_off, 2),
    }
    logger.info("Функция успешно завершила свою работу.")
    return json.dumps(data_to_json, ensure_ascii=False)
