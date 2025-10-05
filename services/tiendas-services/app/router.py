from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import date
from model import Tienda
from .dynamodb import *
# Se crea un APIRouter para agrupar las rutas de tiendas
router = APIRouter(
    prefix="/tiendas",
    tags=["tiendas"],
    responses={404: {"description": "Tienda no encontrada"}},
)

@router.get("/", response_model=List[Tienda])
def obtener_todas_las_tiendas(limit: int = 200):
    items = db.scan_tiendas(limit=limit)
    return [Tienda.from_item(i) for i in items]


@router.get("/{tienda_id}", response_model=Tienda)
def obtener_tienda_por_id(tienda_id: str):
    item = db.get_tienda(tienda_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tienda no encontrada")
    return Tienda.from_item(item)


@router.post("/", response_model=Tienda, status_code=status.HTTP_201_CREATED)
def crear_tienda(tienda: Tienda):
    try:
        db.put_tienda(tienda.to_item())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe una tienda con este ID o error: {e}")
    return tienda


@router.put("/{tienda_id}", response_model=Tienda)
def actualizar_tienda(tienda_id: str, tienda_actualizada: Tienda):
    if tienda_actualizada.tienda_id != tienda_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tienda_id del body debe coincidir con la ruta")
    db.overwrite_tienda(tienda_actualizada.to_item())
    return tienda_actualizada


@router.delete("/{tienda_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tienda(tienda_id: str):
    if not db.get_tienda(tienda_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tienda no encontrada")
    db.delete_tienda(tienda_id)
    return