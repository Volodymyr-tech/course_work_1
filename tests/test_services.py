import pandas as pd

from src.services import df_to_dict, transfers_and_cash_grouped


def test_df_to_dict():
    data = {"Категория": ["Переводы", "Наличные"], "Описание": ["Перевод Иван И.", "Снятие наличных"]}
    df = pd.DataFrame(data)
    result = df_to_dict(df)
    assert isinstance(result, dict)


def test_transfers_and_cash_grouped():
    data = {"Категория": {0: "Переводы", 1: "Наличные"}, "Описание": {0: "Перевод Иван И.", 1: "Снятие наличных"}}
    result = transfers_and_cash_grouped(data)
    assert "Перевод Иван И." in result
