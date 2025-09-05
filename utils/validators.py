# utils/validators.py
# Funciones auxiliares para validar entrada de usuario desde consola.
# Mantener estos validadores separados mejora la limpieza de main.py.

def input_non_empty(prompt: str) -> str:
    """
    Pide una cadena no vacía.
    - Repite hasta que el usuario ingrese algo distinto de espacios en blanco.
    """
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Entrada vacía. Intente de nuevo.")

def input_float_pos(prompt: str) -> float:
    """
    Pide un número flotante positivo.
    - Acepta coma como separador decimal y la convierte a punto.
    """
    while True:
        try:
            v = float(input(prompt).replace(',', '.'))
            if v > 0:
                return v
            print("Debe ser un número positivo.")
        except ValueError:
            print("Ingrese un número válido.")

def input_int_pos(prompt: str) -> int:
    """
    Pide un entero positivo (> 0).
    """
    while True:
        try:
            v = int(input(prompt))
            if v > 0:
                return v
            print("Debe ser un entero positivo.")
        except ValueError:
            print("Ingrese un entero válido.")
