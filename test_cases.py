# =============================================================================
# test_cases.py — Casos de Prueba y Validación (Componente 4)
# =============================================================================
# Este módulo contiene los 10 casos de prueba del sistema experto.
# Cada caso representa un contribuyente real o realista con distintas
# combinaciones de entradas para validar todos los escenarios posibles.
#
# Casos incluidos:
#   Caso 1  — Servicios, categoría A, situación estable
#   Caso 2  — Servicios, categoría C, recategorización por superficie
#   Caso 3  — Venta, categoría E, riesgo por ingresos altos (zona crítica)
#   Caso 4  — Servicios, alquiler excedido (exclusión R39)
#   Caso 5  — Venta, precio unitario excedido (exclusión R47)
#   Caso 6  — Servicios, ingresos superan el límite del régimen (exclusión R12)
#   Caso 7  — CASO LÍMITE: ingresos al 91% del límite de categoría B
#   Caso 8  — Superficie > 200 m² (exclusión R44)
#   Caso 9  — Energía > 20.000 kWh (exclusión R45)
#   Caso 10 — Venta con 1 empleado: piso de categoría A → B (R48)
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
    # Esperado: Categoría E (venta), Zona Crítica — presiones combinadas alta/alta/media (95.7% / 90.9% / 84.5%)
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
    # Esperado: Categoría B, EXCLUIDO por R47 (precio unitario > límite, CF=1.0)
    # Nota: R47 supersede a R37 — se emite la exclusión dura, no la alerta blanda
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 5 — Vendedor de electrónica (Venta, exclusión precio unitario R47)",
        "actividad":  "venta",
        "ingresos":   13_000_000,     # $13M anuales → categoría B (venta)
        "superficie": 30,             # 30 m² (dentro de límite B: 45 m²)
        "energia":    2_500,          # 2500 kWh (dentro de límite B: 5000 kWh)
        "alquiler":   1_200_000,      # $1.2M anuales (dentro de límite B)
        "precio_unit": 750_000,       # $750K por unidad → SUPERA límite ($613.49K) → R47
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


    # -------------------------------------------------------------------------
    # CASO 8 — Superficie mayor a 200 m² → alerta R44 (exclusión por superficie)
    # El contribuyente tiene ingresos en categoría D, pero su local supera
    # el límite máximo absoluto del régimen (200 m²).
    # Esperado: Categoría D, ALERTA R44 — exclusión por superficie
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 8 — Local grande (Servicios, alerta R44 superficie > 200 m²)",
        "actividad":  "servicios",
        "ingresos":   24_000_000,     # $24M anuales → categoría D
        "superficie": 250,            # 250 m² → SUPERA límite máximo absoluto (200 m²)
        "energia":    8_000,          # 8000 kWh (dentro de límite D: 10000 kWh)
        "alquiler":   2_500_000,      # $2.5M anuales (dentro de límite D)
        "precio_unit": 0,
        "empleados":  0
    },

    # -------------------------------------------------------------------------
    # CASO 9 — Energía mayor a 20.000 kWh → alerta R45 (exclusión por energía)
    # El contribuyente tiene ingresos en categoría E, pero su consumo energético
    # supera el límite máximo absoluto del régimen (20.000 kWh).
    # Esperado: Categoría E, ALERTA R45 — exclusión por energía
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 9 — Taller industrial (Venta, alerta R45 energía > 20.000 kWh)",
        "actividad":  "venta",
        "ingresos":   28_000_000,     # $28M anuales → categoría E (venta)
        "superficie": 100,            # 100 m² (dentro de límite E: 110 m²)
        "energia":    25_000,         # 25000 kWh → SUPERA límite máximo absoluto (20000 kWh)
        "alquiler":   3_000_000,      # $3M anuales (dentro de límite E)
        "precio_unit": 300_000,       # $300K por unidad (dentro del límite)
        "empleados":  2
    },


    # -------------------------------------------------------------------------
    # CASO 10 — Kiosquero con 1 empleado: piso de categoría por empleados
    # Ingresos lo ubican en categoría A, pero tener 1 empleado obliga a subir a B.
    # Esperado: Categoría base = A, Categoría final = B (por R48 — piso empleados)
    # -------------------------------------------------------------------------
    {
        "nombre":     "Caso 10 — Kiosquero (Venta, piso Cat. B por 1 empleado R48)",
        "actividad":  "venta",
        "ingresos":   8_000_000,      # $8M anuales → categoría A por ingresos
        "superficie": 20,             # 20 m² (dentro de límite A: 30 m²)
        "energia":    2_000,          # 2000 kWh (dentro de límite A: 3330 kWh)
        "alquiler":   900_000,        # $900K anuales (dentro de límite A)
        "precio_unit": 150_000,       # $150K por unidad (dentro del límite)
        "empleados":  1               # 1 empleado → piso categoría B (R48)
    },

]