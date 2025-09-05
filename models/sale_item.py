
from dataclasses import dataclass

@dataclass(frozen=True)  # inmutable para evitar errores accidentales
class SaleItem:
    product_id: str  # Referencia al Product.id (no guardamos el objeto completo aquí)
    quantity: int    # Cantidad vendida de ese producto
