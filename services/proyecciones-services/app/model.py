from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal

class ProyeccionInsumo(BaseModel):
    fecha_proyeccion: date = Field(
        ...,
        description="Día en que se estima la demanda de insumos",
        example="2025-10-05"
    )
    tienda_id: str = Field(
        ...,
        description="Identificador único de la tienda",
        example="T001"
    )
    nombre_tienda: str = Field(
        ...,
        description="Nombre descriptivo de la tienda",
        example="Salón Surco Central"
    )
    categoria_insumo: str = Field(
        ..., description="Categoría general del insumo", example="crepas"
    )
    unidad_medida: str = Field(
        ...,
        description="Unidad de medida del insumo",
        example="Base de crepe"
    )
    cantidad_estimada: Decimal = Field(
        ...,
        description="Cantidad estimada en la unidad de medida",
        example=12.50
    )
    semana: str = Field(
        ...,
        description="Semana de proyección",
        example="2025-W41"
    )
    origen_modelo: str = Field(
        ...,
        description="Nombre o versión del modelo que genera la estimación",
        example="Modelo_Ventas_2025_v1"
    )
    fecha_generacion: date = Field(
        ...,
        description="Fecha en la que se generó la estimación",
        example="2025-10-01"
    )
    estado_proyeccion: str = Field(
        ...,
        description="Estado de la estimación",
        example="pendiente"
    )
    cantidad_despachada: Decimal = Field(
        ...,
        description="Cantidad efectivamente enviada desde el centro de distribución",
        example=11.00
    )
    cantidad_consumida_real: Decimal = Field(
        ...,
        description="Cantidad real utilizada del insumo (según cierre del día)",
        example=11.80
    )
    diferencia_vs_real: Decimal = Field(
        ...,
        description="Diferencia entre la cantidad estimada y la cantidad real utilizada",
        example=0.70
    )
    usuario_ajuste: str = Field(
        ...,
        description="Usuario o proceso que realizó el ajuste (si aplica)",
        example="sistema_autajuste"
    )
    fecha_confirmacion: date = Field(
        ...,
        description="Fecha en que se validó la proyección o consumo",
        example="2025-10-06"
    )
    observaciones: Optional[str] = Field(
        None,
        description="Comentarios o incidencias",
        example="Sobrestimado por evento local"
    )
