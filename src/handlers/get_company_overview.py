import json
from datetime import datetime, timezone, timedelta
from src.services.company_data_client import (fetch_company_info,CompanyDataError)
from src.repositories.company_repository import (get_company_info,save_company_info)

def is_stale(item: dict) -> bool:
    updated_at = item.get("updated_at")
    if not updated_at:
        return True
    age = datetime.now(timezone.utc) - datetime.fromisoformat(updated_at)
    return age > timedelta(days=30)

def handler(event, context):
    params = event.get("queryStringParameters") or {}
    ticker = params.get("ticker")

    try:
        cached = get_company_info(ticker)
        if cached and not is_stale(cached):
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": json.dumps(cached),
            }
        new = fetch_company_info(ticker)
        saved = save_company_info(new)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps(saved),
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps(str(e)),
        }