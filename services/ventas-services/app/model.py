from datetime import date
from typing import Literal,Any, Mapping
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
# -----------------------
# Utilidades de conversión
# -----------------------
def _to_ddb(value: Any):
    """Convierte floats->Decimal y date->ISO para DynamoDB."""
    if value is None:
        return None
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, (int, str, bool, Decimal)):
        return value
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {k: _to_ddb(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return type(value)(_to_ddb(v) for v in value)
    # fallback a string
    return str(value)

def _from_ddb(obj: Any):
    """Convierte Decimal->float para volver a objetos Python normales."""
    if isinstance(obj, Decimal):
        # si es entero exacto, devuélvelo como int
        if obj == obj.to_integral_value():
            return int(obj)
        return float(obj)
    if isinstance(obj, Mapping):
        return {k: _from_ddb(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(_from_ddb(v) for v in obj)
    return obj


class Venta(BaseModel):
    """
    Modelo de datos para una venta
    """
    venta_id: str = Field(...,description="Identificador único de la venta (clave primaria).",example="V001")
    fecha: date = Field(...,description="Fecha de la venta.",example="2025-10-04")
    turno: Literal["mañana","tarde","noche"] = Field(...,description="Turno de trabajo")
    codigo_articulo: str = Field(...,description="Código alfanumérico del producto",example="10023")
    descripcion_articulo: str =Field(...,description="Descripción comercial del producto",example="CREPE NUTELLA FRESA")
    unidades_total_articulo: int =Field(...,description="Total de unidades ventidas del artículo",example=2)
    categoria_articulo: str = Field(...,description="Categoría del artículo",example="CREPES DULCES")
    origen_pedido: Literal["SALON","RAPPI","PARA LLEVAR","APP"] = Field(...,description="Canal de origen del pedido",example="SALON")
    medio_pago: Literal["EFECTIVO","TARJETA","YAPE","PLIN"] = Field(...,description="Medio de pago utilizado",example="EFECTIVO")
    tienda_id:str = Field(...,description="Identificador único de la tienda",example="T001")
    nombre_tienda:str = Field(...,description="Nombre o ubicación de la tienda",example="Salón Surco Central")
    total: Decimal =Field(...,description="Monto total de la venta (en moneda local)",example=42.5)
    documento:Literal["Boleta","Factura"]=Field(...,description="Tipo de comprobante emitido",example="Boleta")

    @field_validator("fecha", mode="before")
    @classmethod
    def parse_fecha(cls, v):
        if isinstance(v, date):
            return v
        # acepta 'YYYY-MM-DD'
        return date.fromisoformat(str(v))

    # ---- helpers DynamoDB ----
    def to_item(self) -> dict:
        """Item listo para DynamoDB (con Decimals y fecha ISO)."""
        base = {
            "venta_id": self.venta_id,
            "fecha": self.fecha,
            "turno": self.turno,
            "codigo_articulo": self.codigo_articulo,
            "descripcion_articulo": self.descripcion_articulo,
            "unidades_total_articulo": self.unidades_total_articulo,
            "categoria_articulo": self.categoria_articulo,
            "origen_pedido": self.origen_pedido,
            "medio_pago": self.medio_pago,
            "tienda_id": self.tienda_id,
            "nombre_tienda": self.nombre_tienda,
            "total": self.total,
            "documento": self.documento,
        }
        return _to_ddb(base)

    @classmethod
    def from_item(cls, item: dict) -> "Venta":
        """Construye la Venta desde un item DynamoDB."""
        py = _from_ddb(item)
        return cls(**py)