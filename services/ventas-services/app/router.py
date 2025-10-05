from fastapi import APIRouter, HTTPException, Query
from typing import List,Optional
from datetime import date
from .model import Venta  # Importa el modelo Tienda desde schemas.py
from .dynamodb import VentasRepo
# Se crea un APIRouter para agrupar las rutas de tiendas
router = APIRouter(
    prefix="/ventas",
    tags=["ventas"],
    responses={404: {"description": "Venta no encontrada"}},
)

# ---- Rutas HTTP para las tiendas ----
@router.post("", response_model=dict, status_code=201)
def crear_venta(payload: Venta):
    # Si ya existe, puedes validar antes (GetItem) — opcional
    VentasRepo.put(payload)
    return {"venta_id": payload.venta_id}

@router.get("/{venta_id}", response_model=Venta)
def obtener_venta(venta_id: str):
    venta = VentasRepo.get(venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.delete("/{venta_id}", response_model=dict)
def eliminar_venta(venta_id: str):
    VentasRepo.delete(venta_id)
    return {"deleted": True}

@router.get("", response_model=List[Venta])
def listar_ventas(
    tienda_id: Optional[str] = None,
    fecha_desde: Optional[str] = Query(None, description="YYYY-MM-DD"),
    fecha_hasta: Optional[str] = Query(None, description="YYYY-MM-DD"),
    limit: int = Query(100, ge=1, le=1000),
):
    return VentasRepo.scan(tienda_id=tienda_id, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta, limit=limit)