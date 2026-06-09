# src/services/market_data_client.py

import os
import requests
# from decimal import Decimal
# from src.services.market_data_client import MarketDataError

class CompanyDataError(Exception):
    pass

def fetch_company_info(symbol: str) -> dict:
    api_key = os.environ.get("COMPANY_ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise CompanyDataError("Missing COMPANY_ALPHA_VANTAGE_API_KEY")
    
    response = requests.get("https://www.alphavantage.co/query",
        params={
            "function": "OVERVIEW",
            "symbol": symbol.upper(),
            "apikey": api_key,
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if not data or "Symbol" not in data:
        raise CompanyDataError(f"No company overview found for {symbol}")
        # return {
        #     "ticker": "NAN"
        # }
    return {
        "ticker": data.get("Symbol"),
        "symbol": data.get("Symbol"),
        "name": data.get("Name"),
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "market_cap": data.get("MarketCapitalization"),
        "pe_ratio": data.get("PERatio"),
        "dividend_yield": data.get("DividendYield"),
        "profit_margin": data.get("ProfitMargin"),
        "beta": data.get("Beta"),
        "description": data.get("Description"),
        "source": "alpha_vantage",
    }