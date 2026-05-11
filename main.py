# =============================================================================
# main.py — Punto de entrada del Sistema Experto de Monotributo
# =============================================================================
# Este archivo es el punto de entrada del sistema. Al ejecutarlo:
#
#   python main.py
#
# El programa ofrece dos modos de uso:
#
#   1. MODO INTERACTIVO: el usuario ingresa los datos del contribuyente
#      por consola y recibe el diagnóstico en tiempo real.
#
#   2. MODO CASOS DE PRUEBA: ejecuta automáticamente los casos de prueba
#      predefinidos en test_cases.py y muestra los resultados de todos.
#
# =============================================================================

from expert_system import ejecutar_sistema_experto
from presenter import mostrar_resultado
from test_cases import CASOS_DE_PRUEBA


def menu_principal():
    """Muestra el menú de inicio y gestiona la selección del usuario."""
    print("\n" + "=" * 65)
    print("   SISTEMA EXPERTO DE CATEGORIZACIÓN DE MONOTRIBUTO")
    print("   Basado en normativa ARCA vigente desde 01/02/2026")
    print("=" * 65)
    print("\n  ¿Qué desea hacer?")
    print("  [1] Ingresar datos de un contribuyente (modo interactivo)")
    print("  [2] Ejecutar todos los casos de prueba")
    print("  [3] Ejecutar un caso de prueba específico")
    print("  [0] Salir")
    print()
    return input("  Seleccione una opción: ").strip()


def modo_interactivo():
    """
    Modo interactivo: solicita al usuario los datos del contribuyente
    por consola y ejecuta el sistema experto con esos datos.
    """
    print("\n--- INGRESO DE DATOS DEL CONTRIBUYENTE ---\n")

    nombre = input("  Nombre o identificador del caso: ").strip() or "Caso ingresado"

    # Tipo de actividad
    print("\n  Tipo de actividad:")
    print("  [1] Locación o prestación de servicios")
    print("  [2] Venta de cosas muebles")
    opcion = input("  Seleccione (1 o 2): ").strip()
    actividad = "servicios" if opcion == "1" else "venta"

    # Datos numéricos con validación básica
    ingresos    = _pedir_numero("  Ingresos brutos anuales ($): ")
    superficie  = _pedir_numero("  Superficie afectada (m²): ")
    energia     = _pedir_numero("  Energía eléctrica consumida anual (kWh): ")
    alquiler    = _pedir_numero("  Alquiler devengado anual ($, 0 si no paga): ")
    precio_unit = 0
    if actividad == "venta":
        precio_unit = _pedir_numero("  Precio unitario máximo de venta ($): ")
    empleados   = int(_pedir_numero("  Cantidad de empleados en relación de dependencia: "))

    caso = {
        "nombre":     nombre,
        "actividad":  actividad,
        "ingresos":   ingresos,
        "superficie": superficie,
        "energia":    energia,
        "alquiler":   alquiler,
        "precio_unit": precio_unit,
        "empleados":  empleados
    }

    resultado = ejecutar_sistema_experto(caso)
    mostrar_resultado(resultado)


def _pedir_numero(mensaje):
    """Solicita un número al usuario con validación básica."""
    while True:
        try:
            valor = float(input(mensaje).replace(",", ".").replace("$", "").replace(" ", ""))
            return valor
        except ValueError:
            print("  ⚠️  Por favor ingrese un número válido.")


def ejecutar_todos_los_casos():
    """Ejecuta los 7 casos de prueba predefinidos y muestra todos los resultados."""
    print(f"\n  Ejecutando {len(CASOS_DE_PRUEBA)} casos de prueba...\n")
    for caso in CASOS_DE_PRUEBA:
        resultado = ejecutar_sistema_experto(caso)
        mostrar_resultado(resultado)
    print(f"  ✅ {len(CASOS_DE_PRUEBA)} casos de prueba completados.\n")


def ejecutar_caso_especifico():
    """Permite al usuario seleccionar y ejecutar un caso de prueba individual."""
    print("\n  Casos de prueba disponibles:\n")
    for i, caso in enumerate(CASOS_DE_PRUEBA, 1):
        print(f"  [{i}] {caso['nombre']}")
    print()
    try:
        seleccion = int(input("  Seleccione el número del caso: ").strip())
        if 1 <= seleccion <= len(CASOS_DE_PRUEBA):
            caso = CASOS_DE_PRUEBA[seleccion - 1]
            resultado = ejecutar_sistema_experto(caso)
            mostrar_resultado(resultado)
        else:
            print("  ⚠️  Número de caso inválido.")
    except ValueError:
        print("  ⚠️  Ingrese un número válido.")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    while True:
        opcion = menu_principal()

        if opcion == "1":
            modo_interactivo()
        elif opcion == "2":
            ejecutar_todos_los_casos()
        elif opcion == "3":
            ejecutar_caso_especifico()
        elif opcion == "0":
            print("\n  Hasta luego.\n")
            break
        else:
            print("\n  ⚠️  Opción inválida. Intente nuevamente.")