import logging
from src.xlsx_reader import pandas_reader_xlsx
import re
import json
import os

# Указываем путь, который создаст папку "data" внутри текущей директории
log_dir = os.path.join(os.getcwd(), "data")

# Создаем папку, если она не существует
os.makedirs(log_dir, exist_ok=True)

# Путь к лог-файлу
file_path = os.path.join(log_dir, "info.log")

logging.basicConfig(
    filename=file_path,
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)
services_logger = logging.getLogger("transfers_and_cash_grouped")

def df_to_dict(df):
    return df.to_dict(orient="dict")

def transfers_and_cash_grouped(data):
    pattern = r'[А-Яа-яA-Za-z]+\s[А-Яа-яA-Za-z]\.'
    new_data = []
    # Проходим по строкам словаря
    for idx, category in data['Категория'].items():
        if category == 'Переводы':
            description = data['Описание'][idx]  # Получаем описание этой строки

            services_logger.info(f"Проверяем категорию: {category}, описание: {description}")

            if re.search(pattern, description, re.IGNORECASE):  # Проверяем описание
                new_data.append(description)
                services_logger.info(f"Совпадение найдено: {description}")
            else:
                services_logger.error(f"Совпадение не найдено для описания: {description}")

    return new_data


if __name__ == '__main__':
    data_fraime = pandas_reader_xlsx(path = r"C:\Users\Владимир\PycharmProjects\pythonProject1\data\operations.xlsx")
    dict_maker = df_to_dict(data_fraime)
    print(type(dict_maker))
    result = transfers_and_cash_grouped(dict_maker)
    print(result)
