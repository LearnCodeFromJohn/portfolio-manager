import os
import requests
from decimal import Decimal


class MarketDataError(Exception):
    pass


def fetch_daily_prices(symbol: str) -> list[dict]:
    api_key = os.environ["PRICES_ALPHA_VANTAGE_API_KEY"]
    if not api_key:
        raise MarketDataError("Missing PRICES_ALPHA_VANTAGE_API_KEY")

    response = requests.get("https://www.alphavantage.co/query",
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol.upper(),
            "apikey": api_key,
            "outputsize": "compact",
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if "Note" in data:
        raise MarketDataError("API limit exceeded")
    if "Error Message" in data:
        raise MarketDataError(f"Error fetching data for symbol: {symbol}")
    time_series = data.get("Time Series (Daily)")
    if not time_series:
        print("ALPHA VANTAGE RESPONSE:", data)
        raise MarketDataError("time series data not found in response")

    prices = []
    for date, values in time_series.items():
        print('values', values)
        close_price = Decimal(values["4. close"])
        prices.append({
            "ticker": symbol.upper(),
            "date": date,
            "price": close_price,
            "open": Decimal(values["1. open"]),
            "high": Decimal(values["2. high"]),
            "low": Decimal(values["3. low"]),
            # "close": Decimal(values["4, close"]),
            "volume": int(values["5. volume"]),
        })
    return prices