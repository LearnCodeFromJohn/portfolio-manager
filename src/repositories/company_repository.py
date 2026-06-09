# src/repositories/company_repository.py
import os
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb",region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
table = dynamodb.Table(os.environ.get("COMPANY_OVERVIEWS_TABLE", "company_overviews"))

def get_company_info(symbol: str) -> dict | None:
    response = table.get_item(Key={"ticker": symbol.upper()})
    return response.get("Item")

def save_company_info(overview: dict) -> dict:
    item = {
        **overview,
        "ticker": overview["ticker"].upper(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item