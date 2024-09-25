import datetime

from src.utils import get_date_range, start_of_month, start_of_week, start_of_year


def test_start_of_week():
    date = datetime.date(2024, 9, 23)
    result = start_of_week(date)
    assert result == datetime.date(2024, 9, 23)


def test_start_of_month():
    date = datetime.date(2024, 9, 23)
    result = start_of_month(date)
    assert result == datetime.date(2024, 9, 1)


def test_start_of_year():
    date = datetime.date(2024, 9, 23)
    result = start_of_year(date)
    assert result == datetime.date(2024, 1, 1)


def test_get_date_range_month():
    result = get_date_range("23.09.2024", "M")
    assert result[0] == datetime.date(2024, 9, 1)
    assert result[1] == datetime.date(2024, 9, 23)
