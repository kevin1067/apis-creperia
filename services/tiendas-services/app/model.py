from datetime import date
from typing import Literal
from pydantic import BaseModel, Field

class Tienda(BaseModel):
    """
    Modelo de datos para una tienda.
    """
    tienda_id: str = Field(
        ...,
        description="Identificador único de la tienda (clave primaria).",
        example="T001"
    )
    nombre: str = Field(
        ...,
        description="Nombre comercial o interno de la tienda.",
        example="Salón Surco Central"
    )
    direccion: str = Field(
        ...,
        description="Dirección física completa.",
        example="Av. Constitución 1450"
    )
    ciudad: str = Field(
        ...,
        description="Ciudad donde se encuentra la tienda.",
        example="Surco"
    )
    aforo: int = Field(
        ...,
        description="Capacidad máxima o estimada (personas o m²).",
        example=2500
    )
    tipo_tienda: Literal["Salón", "Express", "Centro Comercial"] = Field(
        ...,
        description="Tipo o categoría de tienda."
    )
    horario_apertura: str = Field(
        ...,
        description="Hora local de apertura en formato HH:MM.",
        example="08:00"
    )
    horario_cierre: str = Field(
        ...,
        description="Hora local de cierre en formato HH:MM.",
        example="22:00"
    )
    estado: Literal["activa", "cerrada", "en mantenimiento"] = Field(
        ...,
        description="Estado operativo de la tienda."
    )
    fecha_actualizacion: date = Field(
        ...,
        description="Fecha de la última actualización del registro.",
        example="2025-10-04"
    )
"""
    class Config:
        schema_extra = {
            "example": {
                "tienda_id": "T001",
                "nombre": "Salón Surco Central",
                "direccion": "Av. Constitución 1450",
                "ciudad": "Surco",
                "aforo": 2500,
                "tipo_tienda": "Salón",
                "horario_apertura": "08:00",
                "horario_cierre": "22:00",
                "estado": "activa",
                "fecha_actualizacion": "2025-10-04"
            }
        }"""