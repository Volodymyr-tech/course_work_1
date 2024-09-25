import json
import logging
from src.xlsx_reader import pandas_reader_xlsx
import re
import logging
from config import SERVICES_LOGS

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(SERVICES_LOGS, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def df_to_dict(df):
    return df.to_dict(orient="dict")


def transfers_and_cash_grouped(data):
    pattern = r"[А-Яа-яA-Za-z]+\s[А-Яа-яA-Za-z]\."
    new_data = []
    # Проходим по строкам словаря
    for idx, category in data["Категория"].items():
        if category == "Переводы":
            description = data["Описание"][idx]  # Получаем описание этой строки

            logger.info(f"Проверяем категорию: {category}, описание: {description}")

            if re.search(pattern, description, re.IGNORECASE):  # Проверяем описание
                new_data.append(description)
                logger.info(f"Совпадение найдено: {description}")
            else:
                logger.error(f"Совпадение не найдено для описания: {description}")

    return json.dumps(new_data, ensure_ascii=False)
