import json
from unittest.mock import patch

from src.handlers.get_company_overview import handler
def test_get_company_info_returns_cached_data_when_fresh():
    event = {
        "queryStringParameters": {
            "ticker": "AAPL"
        }
    }
    cached_overview = {
        "ticker": "AAPL",
        "symbol": "AAPL",
        "name": "Apple Inc",
        "sector": "TECHNOLOGY",
        "industry": "CONSUMER ELECTRONICS",
        "updated_at": "2099-01-01T00:00:00+00:00",
    }

    with patch("src.handlers.get_company_overview.get_company_overview") as mock_get, \
         patch("src.handlers.get_company_overview.fetch_company_overview") as mock_fetch:

        mock_get.return_value = cached_overview

        response = handler(event, None)
        body = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert body["ticker"] == "AAPL"
        assert body["name"] == "Apple Inc"

        mock_fetch.assert_not_called()


def test_get_company_info_missing_ticker_returns_400():
    event = {
        "queryStringParameters": {}
    }

    response = handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["error"] == "ticker is required"