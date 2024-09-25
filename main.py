import os

from src.report import spending_by_workday
from src.services import df_to_dict, transfers_and_cash_grouped
from src.utils import get_date_range
from src.views import calculate_expenses
from src.xlsx_reader import pandas_reader_xlsx

if __name__ == "__main__":
    # Получаем от пользователя дату
    user_date = input("Введите дату (в формате дд.мм.гггг):\n")

    # Получаем диапазон фильтрации
    user_range = input(
        "Введите диапазон для фильтрации\nW — неделя\nM — месяц\nY — год\nALL — все данные до даты\n"
    ).upper()
    if user_range not in ["W", "M", "Y", "ALL", ""]:
        print("Неверный диапазон. Используем диапазон по умолчанию — месяц.")
        user_range = "M"

    # Получаем фильтр по дате
    get_range_filter = get_date_range(user_date, user_range)

    # Чтение данных из файла operations.xlsx
    file_path = os.path.join(os.getcwd(), r"data\operations.xlsx")
    data_fraime = pandas_reader_xlsx(file_path)

    # Вычисление расходов
    json_data_expenses = calculate_expenses(data_fraime, *get_range_filter)
    print(json_data_expenses)

    # Запрос у пользователя, хочет ли он вывести список переводов
    user_choose = input("Хотите вывести список переводов для физических лиц? (да/нет)\n").lower()
    if user_choose == "да":
        df_transfer_kash = df_to_dict(data_fraime)
        result_transfer_kash = transfers_and_cash_grouped(df_transfer_kash)
        print(result_transfer_kash)

    # Запрос на вывод среднего значения трат
    user_spend = input(
        "Хотите вывести средние траты в выходные и рабочие дни за последние 3 месяца? (да/нет)\n"
    ).lower()
    if user_spend == "да":
        user_spend_date = input(
            "Введите дату (в формате дд.мм.гггг).\n"
            "Функция выведет средние траты в рабочий и выходной день за последние 3 месяца\n"
        )
        try:
            # Проверка даты
            result_spend_work_and_day_off = spending_by_workday(data_fraime, user_spend_date)
            print(result_spend_work_and_day_off)
        except ValueError:
            print("Неверный формат даты.")
