from unittest.mock import patch
from src.utils import stock_rates

@patch("requests.get")
def test_stock_rates(mock_get):

    mock_get.return_value.json.return_value = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "05. price": "150.12"
        }
    }

    expected_result = [
        {"stock": "AAPL", "price": 150.12}
    ]

    result = stock_rates(["AAPL"])
    assert result == expected_result
