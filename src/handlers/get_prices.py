import json
from decimal import Decimal
from datetime import datetime, timedelta, timezone
from src.services.market_data_client import fetch_daily_prices, MarketDataError
from src.repositories.price_repository import (get_prices_by_symbol,save_missing_prices)

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(body, default=decimal_to_float),
    } 

def is_data_fresh(existing_prices: list[dict]) -> bool:
    if not existing_prices:
        return False
    
    latest_cached_date = datetime.strptime(
        existing_prices[0]["date"],
        "%Y-%m-%d"
    )
    now = datetime.now(timezone.utc)
    # COMMENT
    if now.weekday() < 5:
        return latest_cached_date.date() == now.date()
    else:
        return (now - latest_cached_date) < timedelta(days=3)

def handler(event, context):
    params = event.get("queryStringParameters") or {}
    ticker = params.get("ticker")

    if not ticker:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "ticker is required"}, default=decimal_to_float),
        }
    ticker = ticker.upper()
    
    try:
        existing_prices = get_prices_by_symbol(ticker)
        existing_dates = {p["date"] for p in existing_prices}

        if is_data_fresh(existing_prices):
            return response(200, {
                "ticker": ticker,
                "count": len(existing_prices),
                "source": "cache",
                "new_records_saved": 0,
                "prices": existing_prices,
            })

        fresh_prices = fetch_daily_prices(ticker)
        saved_count = save_missing_prices(fresh_prices, existing_dates)
        final_prices = get_prices_by_symbol(ticker)

        return response(200, {
            "ticker": ticker,
            "count": len(final_prices),
            "source": "api",
            "new_records_saved": saved_count,
            "prices": final_prices,
        })

    except MarketDataError as e:
        print("GET PRICES ERROR:", str(e))

    except Exception as e:
        print("GET PRICES ERROR:", str(e))
        return response(500, {"error": "Failed to get prices"})