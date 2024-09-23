import datetime
from typing import  Optional
import pandas as pd
from dateutil.relativedelta import relativedelta
from src.xlsx_reader import pandas_reader_xlsx


def spending_by_workday(transactions: pd.DataFrame, date_: Optional[str] = None) -> pd.DataFrame:
    if date_ is None:
        date_ = datetime.datetime.now().date()
        start_date = date_ - relativedelta(months=3)

    elif isinstance(date_, str):
        date_ = datetime.datetime.strptime(date_,'%d.%m.%Y').date()
        start_date = date_ - relativedelta(months=3) # Отнимаем 3 месяца от текущей даты.

    transactions_filtered = transactions[transactions["Дата платежа"].notnull()]  # Убираем пустые строки без даты

    transactions_filtered["Дата платежа"] = pd.to_datetime(transactions_filtered["Дата платежа"], dayfirst=True) # Преобразуем столбец с датами в datetime


    filtered_df = transactions_filtered[(transactions_filtered["Дата платежа"].dt.date >= start_date) & (transactions_filtered["Дата платежа"].dt.date <= date_)]

    work_day = filtered_df[filtered_df['Дата платежа'].dt.weekday < 5]

    return work_day



if __name__ == "__main__":
    data_fraime = pandas_reader_xlsx(path=r"C:\Users\Владимир\PycharmProjects\pythonProject1\data\operations.xlsx")
    result = spending_by_workday(data_fraime, '31.12.2021')
    print(result)
    print(type(result))