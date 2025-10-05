import os
import boto3
from boto3.dynamodb.conditions import Key

_TABLE_NAME = os.getenv("TIENDAS_TABLE_NAME", "TiendasTable")

ddb = boto3.resource("dynamodb")

def table():
    return ddb.Table(_TABLE_NAME)

# CRUD helpers

def put_tienda(item: dict):
    return table().put_item(
        Item=item,
        ConditionExpression="attribute_not_exists(tienda_id)"
    )

def overwrite_tienda(item: dict):
    return table().put_item(Item=item)

def get_tienda(tienda_id: str):
    res = table().get_item(Key={"tienda_id": tienda_id})
    return res.get("Item")

def delete_tienda(tienda_id: str):
    return table().delete_item(Key={"tienda_id": tienda_id})

def scan_tiendas(limit: int = 100):
    res = table().scan(Limit=limit)
    return res.get("Items", [])

# Query por ciudad si defines un GSI "ciudad-index"

def query_por_ciudad(ciudad: str, limit: int = 100):
    res = table().query(
        IndexName="ciudad-index",
        KeyConditionExpression=Key("ciudad").eq(ciudad),
        Limit=limit,
    )
    return res.get("Items", [])