# =============================================================================
# knowledge_base.py — Base de Conocimiento del SE de Monotributo
# =============================================================================
# Este módulo contiene todos los datos normativos vigentes desde 01/02/2026
# publicados por ARCA (ex AFIP) en www.afip.gob.ar/monotributo/categorias.asp
#
# Aquí se definen:
#   - Los límites de cada categoría (ingresos, superficie, energía, alquiler)
#   - El impuesto integrado mensual por categoría y tipo de actividad
#   - El precio unitario máximo para venta de cosas muebles
#   - Las funciones de membresía para el módulo difuso
# =============================================================================

# -----------------------------------------------------------------------------
# TABLA DE CATEGORÍAS VIGENTES (fuente: ARCA, vigente desde 01/02/2026)
# Cada categoría es un diccionario con sus parámetros máximos permitidos.
# -----------------------------------------------------------------------------
CATEGORIAS = {
    "A": {
        "ingreso_max":    10_277_988.13,
        "superficie_max": 30,
        "energia_max":    3_330,
        "alquiler_max":   2_390_229.80,
        "impuesto_servicios": 4_780.46,
        "impuesto_venta":     4_780.46,
    },
    "B": {
        "ingreso_max":    15_058_447.71,
        "superficie_max": 45,
        "energia_max":    5_000,
        "alquiler_max":   2_390_229.80,
        "impuesto_servicios": 9_082.88,
        "impuesto_venta":     9_082.88,
    },
    "C": {
        "ingreso_max":    21_113_696.52,
        "superficie_max": 60,
        "energia_max":    6_700,
        "alquiler_max":   3_266_647.39,
        "impuesto_servicios": 15_616.17,
        "impuesto_venta":     14_341.38,
    },
    "D": {
        "ingreso_max":    26_212_853.42,
        "superficie_max": 85,
        "energia_max":    10_000,
        "alquiler_max":   3_266_647.39,
        "impuesto_servicios": 25_495.79,
        "impuesto_venta":     23_742.95,
    },
    "E": {
        "ingreso_max":    30_833_964.37,
        "superficie_max": 110,
        "energia_max":    13_000,
        "alquiler_max":   4_143_064.98,
        "impuesto_servicios": 47_804.60,
        "impuesto_venta":     37_924.98,
    },
    "F": {
        "ingreso_max":    38_642_048.36,
        "superficie_max": 150,
        "energia_max":    16_500,
        "alquiler_max":   4_143_064.98,
        "impuesto_servicios": 67_245.13,
        "impuesto_venta":     49_398.08,
    },
    "G": {
        "ingreso_max":    46_211_109.37,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   4_939_808.23,
        "impuesto_servicios": 122_379.76,
        "impuesto_venta":     61_189.87,
    },
    "H": {
        "ingreso_max":    70_113_407.33,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   7_170_689.39,
        "impuesto_servicios": 350_567.04,
        "impuesto_venta":     175_283.51,
    },
    "I": {
        "ingreso_max":    78_479_211.62,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   7_170_689.39,
        "impuesto_servicios": 697_150.35,
        "impuesto_venta":     278_860.14,
    },
    "J": {
        "ingreso_max":    89_872_640.30,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   7_170_689.39,
        "impuesto_servicios": 836_580.42,
        "impuesto_venta":     334_632.18,
    },
    "K": {
        "ingreso_max":   108_357_084.05,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   7_170_689.39,
        "impuesto_servicios": 1_171_212.59,
        "impuesto_venta":     390_404.20,
    },
}

# Orden de las categorías de menor a mayor (usado para recategorización)
ORDEN_CATEGORIAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

# Precio unitario máximo para venta de cosas muebles (todas las categorías)
PRECIO_UNITARIO_MAX = 613_492.31

# Límite máximo de ingresos del régimen (superar esto implica exclusión)
INGRESO_MAX_REGIMEN = 108_357_084.05


# =============================================================================
# FUNCIONES DE MEMBRESÍA PARA EL MÓDULO DIFUSO
# =============================================================================
# Las funciones de membresía traducen un valor numérico (ej: 0.85)
# a un grado de pertenencia a un conjunto difuso (ej: "presión alta = 0.67").
# Se usan funciones trapezoidales porque permiten zonas de pertenencia plena
# (la parte plana) y zonas de transición gradual (los lados inclinados).
# -----------------------------------------------------------------------------

def membresia_trapezoidal(x, a, b, c, d):
    """
    Calcula el grado de pertenencia de x a un trapecio definido por [a, b, c, d].
    
    Forma del trapecio:
        0 si x <= a o x >= d
        sube de 0 a 1 entre a y b  (lado izquierdo)
        1 si b <= x <= c           (parte plana = pertenencia total)
        baja de 1 a 0 entre c y d  (lado derecho)
    
    Parámetros:
        x   : valor a evaluar (entre 0 y 1, representa el porcentaje de presión)
        a,b : inicio y fin de la rampa ascendente
        c,d : inicio y fin de la rampa descendente
    """
    if x <= a or x >= d:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c)
    return 0.0


def membresia_triangular(x, a, b, c):
    """
    Calcula el grado de pertenencia de x a un triángulo definido por [a, b, c].
    
    Forma del triángulo:
        0 si x <= a o x >= c
        sube de 0 a 1 entre a y b
        baja de 1 a 0 entre b y c
    
    Se usa para los conjuntos difusos de la variable de salida (riesgo fiscal).
    """
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0


# -----------------------------------------------------------------------------
# Conjuntos difusos para las variables de ENTRADA (presión: valor entre 0 y 1)
# Cada función devuelve el grado de pertenencia al conjunto "baja", "media" o "alta"
# -----------------------------------------------------------------------------

def presion_baja(p):
    """Pertenencia plena si p <= 0.60, transición entre 0.60 y 0.75, nula si p >= 0.75"""
    return membresia_trapezoidal(p, -0.01, 0.0, 0.60, 0.75)

def presion_media(p):
    """Transición ascendente entre 0.60 y 0.75, plena entre 0.75 y 0.85, descendente hasta 0.95"""
    return membresia_trapezoidal(p, 0.60, 0.75, 0.85, 0.95)

def presion_alta(p):
    """Transición ascendente entre 0.85 y 0.95, pertenencia plena desde 0.95"""
    return membresia_trapezoidal(p, 0.85, 0.95, 1.0, 1.01)


# -----------------------------------------------------------------------------
# Conjuntos difusos para la variable de SALIDA (riesgo fiscal: valor entre 0 y 100)
# -----------------------------------------------------------------------------

def riesgo_estable(x):
    """Zona estable: centro en 12, entre 0 y 25"""
    return membresia_triangular(x, 0, 12, 25)

def riesgo_precaucion(x):
    """Zona de precaución: centro en 37, entre 20 y 50"""
    return membresia_triangular(x, 20, 37, 50)

def riesgo_zona_riesgo(x):
    """Zona de riesgo: centro en 62, entre 45 y 75"""
    return membresia_triangular(x, 45, 62, 75)

def riesgo_critico(x):
    """Zona crítica: centro en 87, entre 70 y 100"""
    return membresia_triangular(x, 70, 87, 100)