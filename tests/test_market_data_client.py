from unittest.mock import patch, Mock
from decimal import Decimal

from src.services.market_data_client import fetch_daily_prices


def test_fetch_daily_prices_parses_alpha_vantage_response(monkeypatch):
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "fake-key")

    fake_response = {
        "Time Series (Daily)": {
            "2026-05-20": {
                "1. open": "100.00",
                "2. high": "110.00",
                "3. low": "95.00",
                "4. close": "105.00",
                "5. volume": "1234567",
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = fake_response
    mock_response.raise_for_status.return_value = None

    with patch("src.services.market_data_client.requests.get", return_value=mock_response):
        prices = fetch_daily_prices("AAPL")

    assert len(prices) == 1
    assert prices[0]["ticker"] == "AAPL"
    assert prices[0]["date"] == "2026-05-20"
    assert prices[0]["close"] == Decimal("105.00")
    assert prices[0]["volume"] == 1234567