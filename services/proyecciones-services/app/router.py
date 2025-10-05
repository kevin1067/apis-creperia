from fastapi import APIRouter, HTTPException
from typing import List
from model import ProyeccionInsumo
from uuid import uuid4
from datetime import date
from decimal import Decimal

router = APIRouter(
    prefix="/proyecciones",
    tags=["proyecciones"],
    responses={404: {"description": "Proyección no encontrada"}},
)

# Simulación de almacenamiento en memoria
db_proyecciones: List[ProyeccionInsumo] = []

@router.post("/registrar", response_model=ProyeccionInsumo, summary="Registrar proyección")
def crear_proyeccion(proyeccion: ProyeccionInsumo):
    db_proyecciones.append(proyeccion)
    return proyeccion

@router.get("/listar", response_model=List[ProyeccionInsumo], summary="Listar todas las proyecciones")
def listar_proyecciones():
    return db_proyecciones

@router.get("/listar/{tienda_id}", response_model=List[ProyeccionInsumo], summary="Obtener proyecciones por tienda")
def obtener_por_tienda(tienda_id: str):
    resultado = [p for p in db_proyecciones if p.tienda_id == tienda_id]
    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontraron proyecciones para esa tienda")
    return resultado

@router.get("/semana/{semana}", response_model=List[ProyeccionInsumo], summary="Obtener proyecciones por semana")
def obtener_por_semana(semana: str):
    resultado = [p for p in db_proyecciones if p.semana == semana]
    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontraron proyecciones para esa semana")
    return resultado

@router.delete("/eliminar/{tienda_id}/{semana}", summary="Eliminar proyecciones por tienda y semana")
def eliminar_proyeccion(tienda_id: str, semana: str):
    global db_proyecciones
    original_len = len(db_proyecciones)
    db_proyecciones = [p for p in db_proyecciones if not (p.tienda_id == tienda_id and p.semana == semana)]
    if len(db_proyecciones) == original_len:
        raise HTTPException(status_code=404, detail="No se encontró la proyección para eliminar")
    return {"mensaje": "Proyección eliminada"}
"""
@router.post("/generar", response_model=List[ProyeccionInsumo], summary="Generar proyecciones automáticamente")
def generar_proyecciones():
    # Aquí integrar consumo promedio
    tiendas = [{"id": "T001", "nombre": "Salón Surco Central"}, {"id": "T002", "nombre": "Salón Miraflores"}]
    categorias = ["crepas", "waffles"]
    semana = "2025-W41"

    nuevas = []
    for tienda in tiendas:
        for categoria in categorias:
            proyeccion = ProyeccionInsumo(
                fecha_proyeccion=date.fromisoformat("2025-10-05"),
                tienda_id=tienda["id"],
                nombre_tienda=tienda["nombre"],
                categoria_insumo=categoria,
                unidad_medida="Base de crepe",
                cantidad_estimada=Decimal("12.50"),
                semana=semana,
                origen_modelo="Promedio_Historico_v1",
                fecha_generacion=date.today(),
                estado_proyeccion="pendiente",
                cantidad_despachada=Decimal("11.00"),
                cantidad_consumida_real=Decimal("11.80"),
                diferencia_vs_real=Decimal("0.70"),
                usuario_ajuste="sistema_autajuste",
                fecha_confirmacion=date.fromisoformat("2025-10-06"),
                observaciones="Generado automáticamente"
            )
            db_proyecciones.append(proyeccion)
            nuevas.append(proyeccion)
    return nuevas
"""