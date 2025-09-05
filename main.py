
# Importamos el orquestador (servicio) y validadores de entrada
from services.sales_manager import SalesManager
from utils.validators import input_non_empty, input_float_pos, input_int_pos

# Menú principal que verá el usuario
MENU = (
    "\n=== Sistema de Ventas Diarias ===\n"
    "1) Registrar producto\n"
    "2) Registrar venta\n"
    "3) Generar reporte (ordenar por ingresos o cantidad)\n"
    "4) Exportar totales por producto a CSV\n"
    "5) Salir\n"
)

def registrar_producto(manager: SalesManager) -> None:
    """
    Pide datos al usuario para crear un nuevo producto y lo agrega al catálogo.
    """
    print("\n— Registro de producto —")
    nombre = input_non_empty("Nombre del producto: ")  # no permite vacío
    categoria = input("Categoría (opcional): ").strip() or None  # puede ser None
    precio = input_float_pos("Precio unitario ($): ")  # valida número positivo

    # Agregamos el producto al sistema y mostramos confirmación
    prod = manager.add_product(nombre=nombre, price=precio, category=categoria)
    print(f"Producto registrado: {prod.name} (ID={prod.id}, $ {prod.price:.2f})")

def registrar_venta(manager: SalesManager) -> None:
    """
    Permite registrar una venta con múltiples ítems (producto + cantidad).
    """
    print("\n— Registro de venta —")
    if not manager.products:
        # No tiene sentido vender si no hay productos cargados
        print("No hay productos. Registre al menos uno antes de vender.")
        return

    items = []  # almacenará tuplas (product_id, cantidad)
    while True:
        print("\nProductos disponibles:")
        # Listamos catálogo para que el usuario vea IDs y precios
        for p in manager.products.values():
            print(f"  {p.id}) {p.name} — $ {p.price:.2f}")

        pid = input_non_empty("ID de producto (o 'fin' para terminar): ")
        if pid.lower() == 'fin':
            # Terminamos la captura de ítems
            break
        if pid not in manager.products:
            # Validamos que el ID exista en el catálogo
            print("ID inválido. Intente de nuevo.")
            continue
        cantidad = input_int_pos("Cantidad: ")  # entero positivo
        items.append((pid, cantidad))  # guardamos el ítem

    if not items:
        # Si no se ingresaron ítems, no registramos la venta
        print("Venta cancelada: no se agregaron ítems.")
        return

    # Registramos la venta en el sistema y mostramos el total
    sale = manager.record_sale(items)
    print(f"Venta registrada con {len(sale.items)} ítems. Total $ {sale.total(manager.products):.2f}")

def generar_reporte(manager: SalesManager) -> None:
    """
    Genera un resumen por producto (cantidad e ingresos) y
    permite ordenarlo por 'ingresos' o por 'cantidad'.
    """
    if not manager.sales:
        print("No hay ventas registradas.")
        return

    print("\n— Reporte —")
    criterio = input_non_empty("Ordenar por 'ingresos' o 'cantidad': ")
    if criterio not in ("ingresos", "cantidad"):
        print("Criterio inválido. Use 'ingresos' o 'cantidad'.")
        return

    # Obtenemos el resumen y lo ordenamos según el criterio elegido
    resumen = manager.totals_by_product()
    orden = manager.sorted_totals(resumen, key=criterio)

    # Impresión formateada del reporte
    ancho = 62
    print("\n" + "=" * ancho)
    print(f"{'Producto':20} | {'Cantidad':>10} | {'Ingresos ($)':>12}")
    print("-" * ancho)
    for row in orden:
        nombre = row['name'][:20]  # truncamos nombre para alinear columnas
        print(f"{nombre:20} | {row['cantidad']:>10} | {row['ingresos']:>12.2f}")
    print("=" * ancho)

    # Totales generales
    total_ingresos = sum(r['ingresos'] for r in orden)
    total_unidades = sum(r['cantidad'] for r in orden)
    print(f"TOTAL UNIDADES: {total_unidades} — TOTAL INGRESOS: $ {total_ingresos:.2f}")

def exportar_csv(manager: SalesManager) -> None:
    """
    Exporta a un archivo CSV los totales por producto (id, nombre, cantidad, ingresos).
    """
    if not manager.sales:
        print("No hay ventas para exportar.")
        return
    ruta = input_non_empty("Nombre de archivo CSV de salida (p.ej. 'totales.csv'): ")
    count = manager.export_totals_csv(ruta)
    print(f"Se exportaron {count} filas a '{ruta}'.")

def main() -> None:
    """
    Bucle principal de la aplicación (menú).
    """
    manager = SalesManager()  # instancia que gestiona toda la lógica de negocio
    while True:
        print(MENU)
        op = input("Seleccione opción: ").strip()
        if op == "1":
            registrar_producto(manager)
        elif op == "2":
            registrar_venta(manager)
        elif op == "3":
            generar_reporte(manager)
        elif op == "4":
            exportar_csv(manager)
        elif op == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

# Punto de entrada del script
if __name__ == "__main__":
    main()
