
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)  # frozen=True => inmutable (más seguro para el dominio)
class Product:
    id: str            # ID interno (ej.: P1, P2, ...), lo genera SalesManager
    name: str          # Nombre del producto (ej.: Tomate)
    price: float       # Precio unitario en dólares
    category: Optional[str] = None  # Categoría opcional (verduras, granos, etc.)
