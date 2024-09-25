import json

import pandas as pd

from src.report import spending_by_workday


def test_spending_by_workday():
    data = {"Дата платежа": ["01.01.2022", "05.01.2022", "10.01.2022"], "Сумма операции": [-100, -200, -300]}
    df = pd.DataFrame(data)
    result = spending_by_workday(df, "10.01.2022")
    result_json = json.loads(result)
    assert "Средняя трата в рабочий день" in result_json
    assert result_json["Средняя трата в рабочий день"] == -250.0
