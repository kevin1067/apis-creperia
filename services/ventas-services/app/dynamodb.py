import os
from typing import Optional, Dict, Any, List
import boto3
from botocore.config import Config
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from .model import Venta
from botocore.config import Config
_TABLE_NAME = os.environ.get("VENTAS_TABLE", "ventas-table")
REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
# Si corres con serverless offline o definiste DYNAMODB_ENDPOINT, úsalo
ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")
if not ENDPOINT and os.getenv("IS_OFFLINE"):
    ENDPOINT = "http://localhost:8000"

# Si usas DDB local y no tienes credenciales, pon fake para que boto3 no se queje
if ENDPOINT and not os.getenv("AWS_ACCESS_KEY_ID"):
    os.environ.setdefault("AWS_ACCESS_KEY_ID", "fake")
    os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "fake")

_session = boto3.session.Session(region_name=REGION)
_dynamodb = _session.resource(
    "dynamodb",
    config=Config(retries={"max_attempts": 10, "mode": "standard"})
)
table = _dynamodb.Table(_TABLE_NAME)

class VentasRepo:

    @staticmethod
    def put(venta: Venta) -> Dict[str, Any]:
        try:
            table.put_item(Item=venta.to_item())
            return {"venta_id": venta.venta_id}
        except ClientError as e:
            raise RuntimeError(f"DynamoDB put_item error: {e.response['Error']['Message']}")

    @staticmethod
    def get(venta_id: str) -> Optional[Venta]:
        try:
            resp = table.get_item(Key={"venta_id": venta_id})
        except ClientError as e:
            # tabla no encontrada, permisos, etc.
            raise RuntimeError(f"DynamoDB get_item error: {e.response['Error']['Message']}")
        item = resp.get("Item")
        if not item:
            return None
        return Venta.from_item(item)

    @staticmethod
    def delete(venta_id: str) -> bool:
        try:
            table.delete_item(Key={"venta_id": venta_id})
            return True
        except ClientError as e:
            raise RuntimeError(f"DynamoDB delete_item error: {e.response['Error']['Message']}")

    @staticmethod
    def scan(tienda_id: Optional[str]=None, fecha_desde: Optional[str]=None,
             fecha_hasta: Optional[str]=None, limit: int = 100) -> List[Venta]:
        fe = None
        if tienda_id:
            fe = Attr("tienda_id").eq(tienda_id)
        if fecha_desde:
            fe = (fe & Attr("fecha").gte(fecha_desde)) if fe is not None else Attr("fecha").gte(fecha_desde)
        if fecha_hasta:
            fe = (fe & Attr("fecha").lte(fecha_hasta)) if fe is not None else Attr("fecha").lte(fecha_hasta)

        params = {"Limit": limit}
        if fe is not None:
            params["FilterExpression"] = fe

        try:
            items, resp = [], table.scan(**params)
            items.extend(resp.get("Items", []))
            while "LastEvaluatedKey" in resp and len(items) < limit:
                params["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
                resp = table.scan(**params)
                items.extend(resp.get("Items", []))
        except ClientError as e:
            raise RuntimeError(f"DynamoDB scan error: {e.response['Error']['Message']}")
        return [Venta.from_item(it) for it in items[:limit]]