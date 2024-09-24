import pytest
from src.xlsx_reader import pandas_reader_xlsx
import os
from config import DATA_DIR
import pandas as pd

def test_pandas_reader_xlsx_valid_path():
    path = os.path.join(DATA_DIR,"operations.xlsx")
    result = pandas_reader_xlsx(path)
    assert isinstance(result, pd.DataFrame), "Ожидается, что результат будет DataFrame"

def test_pandas_reader_xlsx_invalid_path():
    result = pandas_reader_xlsx("non_existent_file.xlsx")
    assert result == [], "Ожидается, что результат будет пустым списком при отсутствии файла"