# =============================================================================
# test_cases.py — Casos de Prueba y Validación (Componente 4)
# =============================================================================
# Este módulo contiene los 7 casos de prueba del sistema experto.
# Cada caso representa un contribuyente real o realista con distintas
# combinaciones de entradas para validar todos los escenarios posibles.
#
# Casos incluidos:
#   Caso 1 — Servicios, categoría A, situación estable
#   Caso 2 — Servicios, categoría C, recategorización por superficie
#   Caso 3 — Venta, categoría E, riesgo por ingresos altos
#   Caso 4 — Servicios, alquiler excedido (alerta de exclusión)
#   Caso 5 — Venta, precio unitario excedido (alerta)
#   Caso 6 — Servicios, ingresos superan el límite del régimen (exclusión)
#   Caso 7 — CASO LÍMITE: ingresos exactamente al 91% del límite de categoría B
# =============================================================================

CASOS_DE_PRUEBA = [

    # -------------------------------------------------------------------------
    # CASO 1 — Diseñador gráfico independiente, categoría A, situación cómoda
    # Esperado: Categoría A, Situación Estable
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 1 — Diseñador gráfico (Servicios, Cat. A)",
        "actividad":  "servicios",
        "ingresos":   6_500_000,      # $6.5M anuales (límite cat A: $10.27M)
        "superficie": 15,             # 15 m² (límite cat A: 30 m²)
        "energia":    1_200,          # 1200 kWh (límite cat A: 3330 kWh)
        "alquiler":   800_000,        # $800K anuales (límite cat A: $2.39M)
        "precio_unit": 0,             # No aplica para servicios
        "empleados":  0
    },

    # -------------------------------------------------------------------------
    # CASO 2 — Contador con oficina grande, recategorización por superficie
    # Esperado: Categoría por ingresos = B, Categoría final = C (por superficie)
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 2 — Contador con oficina (Servicios, recategorización superficie)",
        "actividad":  "servicios",
        "ingresos":   12_000_000,     # $12M anuales → categoría B por ingresos
        "superficie": 50,             # 50 m² → supera límite de B (45 m²) → sube a C
        "energia":    3_000,          # 3000 kWh (dentro de límite B: 5000 kWh)
        "alquiler":   1_500_000,      # $1.5M anuales (dentro de límite B)
        "precio_unit": 0,
        "empleados":  0
    },

    # -------------------------------------------------------------------------
    # CASO 3 — Comerciante de ropa, categoría E, ingresos cerca del límite
    # Esperado: Categoría E (venta), Zona de Riesgo por presión de ingresos alta
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 3 — Comerciante de ropa (Venta, Cat. E, riesgo alto)",
        "actividad":  "venta",
        "ingresos":   29_500_000,     # $29.5M anuales (límite cat E: $30.83M → 95.6%)
        "superficie": 100,            # 100 m² (límite cat E: 110 m²)
        "energia":    11_000,         # 11000 kWh (límite cat E: 13000 kWh)
        "alquiler":   3_500_000,      # $3.5M anuales (límite cat E: $4.14M)
        "precio_unit": 450_000,       # $450K por unidad (límite: $613K → ok)
        "empleados":  1
    },

    # -------------------------------------------------------------------------
    # CASO 4 — Odontóloga con consultorio alquilado a precio alto
    # Esperado: Categoría D, ALERTA por alquiler excedido
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 4 — Odontóloga (Servicios, alerta alquiler excedido)",
        "actividad":  "servicios",
        "ingresos":   24_000_000,     # $24M anuales → categoría D
        "superficie": 70,             # 70 m² (dentro de límite D: 85 m²)
        "energia":    5_000,          # 5000 kWh (dentro de límite D: 10000 kWh)
        "alquiler":   4_000_000,      # $4M anuales → SUPERA límite cat D ($3.26M)
        "precio_unit": 0,
        "empleados":  0
    },

    # -------------------------------------------------------------------------
    # CASO 5 — Vendedor de electrónica, precio unitario excedido
    # Esperado: Categoría B (venta), ALERTA por precio unitario
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 5 — Vendedor de electrónica (Venta, alerta precio unitario)",
        "actividad":  "venta",
        "ingresos":   13_000_000,     # $13M anuales → categoría B (venta)
        "superficie": 30,             # 30 m² (dentro de límite B: 45 m²)
        "energia":    2_500,          # 2500 kWh (dentro de límite B: 5000 kWh)
        "alquiler":   1_200_000,      # $1.2M anuales (dentro de límite B)
        "precio_unit": 750_000,       # $750K por unidad → SUPERA límite ($613.49K)
        "empleados":  0
    },

    # -------------------------------------------------------------------------
    # CASO 6 — Médico especialista con ingresos que superan el régimen
    # Esperado: EXCLUSIÓN del Monotributo, debe pasar al Régimen General
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 6 — Médico especialista (Exclusión del régimen)",
        "actividad":  "servicios",
        "ingresos":   120_000_000,    # $120M anuales → SUPERA límite máximo ($108.35M)
        "superficie": 40,
        "energia":    4_000,
        "alquiler":   2_000_000,
        "precio_unit": 0,
        "empleados":  1
    },

    # -------------------------------------------------------------------------
    # CASO 7 — CASO LÍMITE: ingresos al 91% del límite de categoría B
    # Este es el caso ambiguo: no está excluido pero está en zona gris.
    # Esperado: Categoría B, Zona de Precaución o Riesgo (depende del módulo difuso)
    # Análisis: el sistema debería capturar la gradualidad sin alarmar en exceso
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 7 (LÍMITE) — Electricista al 91% del límite Cat. B",
        "actividad":  "servicios",
        "ingresos":   13_703_187,     # 91% de $15.058.447 (límite cat B)
        "superficie": 25,             # Cómodo dentro de límite B (45 m²)
        "energia":    3_200,          # Cómodo dentro de límite B (5000 kWh)
        "alquiler":   900_000,        # Cómodo dentro de límite B ($2.39M)
        "precio_unit": 0,
        "empleados":  0
    },

]