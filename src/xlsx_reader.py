from typing import Any, Dict, List, Union

import pandas as pd


def pandas_reader_xlsx(path: str) -> Union[Dict[str, Any], List[Any]]:
    """Функция для чтения XLSX файла в виде словаря"""
    try:
        reader = pd.read_excel(path, index_col=0)
        return reader

    except FileNotFoundError:
        print("Файл не найден.")
        return []
