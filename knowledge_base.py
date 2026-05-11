# =============================================================================
# knowledge_base.py — Datos Normativos del SE de Monotributo
# =============================================================================
# Responsabilidad única: almacenar los datos normativos vigentes.
# Es el único archivo que debe actualizarse cuando ARCA modifica sus tablas.
# No contiene lógica computacional — las funciones de membresía difusa
# están en fuzzy_membership.py.
#
# Fuente: ARCA (ex AFIP) — www.afip.gob.ar/monotributo/categorias.asp
# Vigente desde: 01/02/2026
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
        "sipa":               15_616.17,
        "obra_social":        21_990.11,
    },
    "B": {
        "ingreso_max":    15_058_447.71,
        "superficie_max": 45,
        "energia_max":    5_000,
        "alquiler_max":   2_390_229.80,
        "impuesto_servicios": 9_082.88,
        "impuesto_venta":     9_082.88,
        "sipa":               17_177.79,
        "obra_social":        21_990.11,
    },
    "C": {
        "ingreso_max":    21_113_696.52,
        "superficie_max": 60,
        "energia_max":    6_700,
        "alquiler_max":   3_266_647.39,
        "impuesto_servicios": 15_616.17,
        "impuesto_venta":     14_341.38,
        "sipa":               18_895.57,
        "obra_social":        21_990.11,
    },
    "D": {
        "ingreso_max":    26_212_853.42,
        "superficie_max": 85,
        "energia_max":    10_000,
        "alquiler_max":   3_266_647.39,
        "impuesto_servicios": 25_495.79,
        "impuesto_venta":     23_742.95,
        "sipa":               20_785.13,
        "obra_social":        26_133.18,
    },
    "E": {
        "ingreso_max":    30_833_964.37,
        "superficie_max": 110,
        "energia_max":    13_000,
        "alquiler_max":   4_143_064.98,
        "impuesto_servicios": 47_804.60,
        "impuesto_venta":     37_924.98,
        "sipa":               22_863.64,
        "obra_social":        31_869.73,
    },
    "F": {
        "ingreso_max":    38_642_048.36,
        "superficie_max": 150,
        "energia_max":    16_500,
        "alquiler_max":   4_143_064.98,
        "impuesto_servicios": 67_245.13,
        "impuesto_venta":     49_398.08,
        "sipa":               25_150.00,
        "obra_social":        36_650.19,
    },
    "G": {
        "ingreso_max":    46_211_109.37,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   4_939_808.23,
        "impuesto_servicios": 122_379.76,
        "impuesto_venta":     61_189.87,
        "sipa":               35_210.00,
        "obra_social":        39_518.47,
    },
    "H": {
        "ingreso_max":    70_113_407.33,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   7_170_689.39,
        "impuesto_servicios": 350_567.04,
        "impuesto_venta":     175_283.51,
        "sipa":               49_294.00,
        "obra_social":        47_485.89,
    },
    "I": {
        "ingreso_max":    78_479_211.62,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   7_170_689.39,
        "impuesto_servicios": 697_150.35,
        "impuesto_venta":     278_860.14,
        "sipa":               69_011.60,
        "obra_social":        58_640.31,
    },
    "J": {
        "ingreso_max":    89_872_640.30,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   7_170_689.39,
        "impuesto_servicios": 836_580.42,
        "impuesto_venta":     334_632.18,
        "sipa":               96_616.24,
        "obra_social":        65_810.99,
    },
    "K": {
        "ingreso_max":   108_357_084.05,
        "superficie_max": 200,
        "energia_max":    20_000,
        "alquiler_max":   7_170_689.39,
        "impuesto_servicios": 1_171_212.59,
        "impuesto_venta":     390_404.20,
        "sipa":               135_262.74,
        "obra_social":        75_212.57,
    },
}

# Orden de las categorías de menor a mayor (usado para recategorización)
ORDEN_CATEGORIAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

# Precio unitario máximo para venta de cosas muebles (todas las categorías)
PRECIO_UNITARIO_MAX = 613_492.31

# Límite máximo de ingresos del régimen (superar esto implica exclusión)
INGRESO_MAX_REGIMEN = 108_357_084.05

# Alquiler máximo global del régimen — umbral de la regla catch-all R46
# (coincide con el límite de las categorías H-K, que es el más alto del régimen)
ALQUILER_MAX_GLOBAL = 7_170_689.39
