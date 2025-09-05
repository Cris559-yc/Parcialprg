
from __future__ import annotations  # para usar anotaciones futuras (| en tipos)
from typing import Dict, List, Tuple
import csv
from models.product import Product
from models.sale_item import SaleItem
from models.sale import Sale

class SalesManager:
    """Coordina productos, ventas y reportes del sistema."""

    def __init__(self) -> None:
        # Catálogo de productos (clave: id tipo 'P1', 'P2'...)
        self.products: Dict[str, Product] = {}
        # Ventas registradas (cada una con sus ítems)
        self.sales: List[Sale] = []
        # Secuencia interna para generar IDs automáticos de productos
        self._seq = 1  # P1, P2, P3, ...

    # ————— Productos —————
    def add_product(self, nombre: str, price: float, category: str | None = None) -> Product:
        """
        Crea un Product y lo agrega al catálogo.
        - Genera un ID único tipo 'P{n}'.
        - Redondea el precio a dos decimales.
        """
        pid = f"P{self._seq}"
        self._seq += 1
        prod = Product(id=pid, name=nombre.strip(), price=round(price, 2), category=category)
        self.products[pid] = prod
        return prod

    # ————— Ventas —————
    def record_sale(self, items: List[Tuple[str, int]]) -> Sale:
        """
        Registra una venta a partir de una lista de tuplas (product_id, cantidad).
        - Valida que existan los productos y que la cantidad sea > 0.
        """
        sale_items = []
        for pid, qty in items:
            if pid not in self.products:
                raise ValueError(f"Producto inexistente: {pid}")
            if qty <= 0:
                raise ValueError("La cantidad debe ser > 0")
            sale_items.append(SaleItem(product_id=pid, quantity=qty))

        sale = Sale(items=sale_items)
        self.sales.append(sale)  # guardamos la venta en el historial
        return sale

    # ————— Reportes —————
    def totals_by_product(self) -> List[Dict]:
        """
        Agrega cantidades e ingresos por producto a través de TODAS las ventas.
        Devuelve una lista de dicts: {id, name, cantidad, ingresos}
        """
        acumulado: Dict[str, Dict] = {}

        for sale in self.sales:
            for it in sale.items:
                p = self.products[it.product_id]  # resolvemos el producto
                if p.id not in acumulado:
                    # Inicializamos acumuladores por producto
                    acumulado[p.id] = {
                        'id': p.id,
                        'name': p.name,
                        'cantidad': 0,
                        'ingresos': 0.0,
                    }
                # Sumamos cantidad e ingresos (precio * cantidad)
                acumulado[p.id]['cantidad'] += it.quantity
                acumulado[p.id]['ingresos'] += p.price * it.quantity

        # Convertimos a lista para facilitar ordenamientos/imprimir
        return list(acumulado.values())

    def sorted_totals(self, rows: List[Dict], key: str) -> List[Dict]:
        """
        Ordena la lista de totales por 'ingresos' o por 'cantidad'.
        - 'reverse=True' para que el mayor quede primero.
        - Desempata por nombre para orden estable y legible.
        """
        if key not in ("ingresos", "cantidad"):
            raise ValueError("key debe ser 'ingresos' o 'cantidad'")
        return sorted(rows, key=lambda r: (r[key], r['name']), reverse=True)

    # ————— Export —————
    def export_totals_csv(self, path: str) -> int:
        """
        Exporta a CSV los totales por producto, ordenados por ingresos.
        Retorna el número de filas escritas (sin contar el header).
        """
        rows = self.totals_by_product()
        rows = self.sorted_totals(rows, key='ingresos')  # ordenamos para el CSV

        # Abrimos archivo en modo escritura con UTF-8 y sin saltos de línea extra
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'cantidad', 'ingresos'])
            writer.writeheader()  # cabecera
            for r in rows:
                writer.writerow(r)  # escribimos cada fila (dict)

        return len(rows)
