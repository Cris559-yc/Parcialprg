
from dataclasses import dataclass, field
from typing import List, Dict
from .sale_item import SaleItem
from .product import Product

@dataclass
class Sale:
    # Lista de líneas (ítems) de la venta
    items: List[SaleItem] = field(default_factory=list)

    def total(self, products: Dict[str, Product]) -> float:
        """
        Calcula el total de la venta sumando (precio * cantidad) por cada ítem.
        - 'products' es un diccionario id->Product para resolver el precio.
        """
        total = 0.0
        for it in self.items:
            p = products[it.product_id]   # buscamos el producto por su ID
            total += p.price * it.quantity
        return total
