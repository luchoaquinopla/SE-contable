# =============================================================================
# fuzzy_engine.py — Motor de Lógica Difusa
# =============================================================================
# Este módulo implementa el Bloque 5 de la base de conocimiento:
# la evaluación del riesgo fiscal global mediante lógica difusa.
#
# ¿Por qué lógica difusa aquí?
#   Un contador no evalúa el riesgo de forma binaria ("seguro" o "en riesgo").
#   Evalúa simultáneamente múltiples indicadores y emite un juicio gradual
#   como "hay que estar atentos" o "situación comprometida".
#   La lógica difusa captura exactamente ese razonamiento gradual.
#
# El módulo funciona en tres pasos:
#   1. FUZZIFICACIÓN: convierte los porcentajes de presión en grados de
#      pertenencia a los conjuntos difusos (baja, media, alta)
#   2. INFERENCIA DIFUSA: aplica las reglas RD1-RD12 usando mínimo (AND)
#   3. DEFUZZIFICACIÓN: convierte la salida difusa en un valor numérico
#      usando el método del centroide (centro de gravedad)
# =============================================================================

import numpy as np
from knowledge_base import CATEGORIAS
from fuzzy_membership import (
    presion_baja, presion_media, presion_alta,
    riesgo_estable, riesgo_precaucion, riesgo_zona_riesgo, riesgo_critico
)


def calcular_presiones(categoria_final, ingresos, superficie, energia, alquiler):
    """
    Calcula las tres variables de presión que alimentan el módulo difuso.
    
    Cada presión es un valor entre 0 y 1 que representa qué porcentaje
    del límite normativo correspondiente ya fue consumido.
    
    Parámetros:
        categoria_final : str — categoría ya ajustada (ej: "C")
        ingresos        : float — ingresos brutos anuales
        superficie      : float — superficie afectada en m²
        energia         : float — energía consumida en kWh
        alquiler        : float — alquiler devengado anual en pesos
    
    Retorna:
        dict con 'presion_ingresos', 'presion_fisica', 'presion_alquiler'
    """
    if categoria_final is None:
        # Si hay exclusión, todas las presiones son máximas
        return {"presion_ingresos": 1.0, "presion_fisica": 1.0, "presion_alquiler": 1.0}

    limites = CATEGORIAS[categoria_final]

    # Presión de ingresos: qué fracción del límite superior ya se usó
    presion_ingresos = min(ingresos / limites["ingreso_max"], 1.0)

    # Presión física: el mayor entre la fracción de superficie y la de energía
    p_superficie = min(superficie / limites["superficie_max"], 1.0) if limites["superficie_max"] > 0 else 0
    p_energia    = min(energia    / limites["energia_max"],    1.0) if limites["energia_max"]    > 0 else 0
    presion_fisica = max(p_superficie, p_energia)

    # Presión de alquiler: qué fracción del límite de alquiler ya se usó
    presion_alquiler = min(alquiler / limites["alquiler_max"], 1.0) if limites["alquiler_max"] > 0 else 0

    return {
        "presion_ingresos": round(presion_ingresos, 4),
        "presion_fisica":   round(presion_fisica,   4),
        "presion_alquiler": round(presion_alquiler, 4)
    }


def fuzzificar(presion_ingresos, presion_fisica, presion_alquiler):
    """
    PASO 1 — Fuzzificación.
    
    Convierte los tres valores numéricos de presión en grados de pertenencia
    a los conjuntos difusos: baja, media y alta.
    
    Por ejemplo: presion_ingresos = 0.85 podría pertenecer a:
        - presion_media con grado 0.67
        - presion_alta  con grado 0.0
    
    Retorna:
        dict con los grados de pertenencia de cada variable
    """
    return {
        "ingresos": {
            "baja":  presion_baja(presion_ingresos),
            "media": presion_media(presion_ingresos),
            "alta":  presion_alta(presion_ingresos),
        },
        "fisica": {
            "baja":  presion_baja(presion_fisica),
            "media": presion_media(presion_fisica),
            "alta":  presion_alta(presion_fisica),
        },
        "alquiler": {
            "baja":  presion_baja(presion_alquiler),
            "media": presion_media(presion_alquiler),
            "alta":  presion_alta(presion_alquiler),
        }
    }


def aplicar_reglas_difusas(grados):
    """
    PASO 2 — Inferencia difusa (Bloque 5: reglas RD1-RD27).

    Cubre las 27 combinaciones posibles (3 variables × 3 valores = 3³).
    Las reglas RD1-RD12 son las del documento original; RD13-RD27 completan
    las combinaciones no cubiertas cuya ausencia causaba activaciones = 0.

    AND = mínimo entre condiciones de una regla.
    OR  = máximo entre reglas con el mismo consecuente.
    """
    i = grados["ingresos"]
    f = grados["fisica"]
    a = grados["alquiler"]

    activaciones = {
        # ── ESTABLE ──────────────────────────────────────────────────────────
        "estable": min(i["baja"], f["baja"], a["baja"]),            # RD1

        # ── PRECAUCIÓN ───────────────────────────────────────────────────────
        "precaucion": max(
            min(i["media"], f["baja"],  a["baja"]),   # RD2
            min(i["baja"],  f["media"], a["baja"]),   # RD3
            min(i["baja"],  f["baja"],  a["media"]),  # RD4
            # Nuevas (RD13-RD15): baja ingresos con presión moderada en otros
            min(i["baja"],  f["baja"],  a["alta"]),   # RD13: B+B+A
            min(i["baja"],  f["media"], a["media"]),  # RD14: B+M+M
            min(i["baja"],  f["alta"],  a["baja"]),   # RD15: B+A+B
        ),

        # ── RIESGO ───────────────────────────────────────────────────────────
        "riesgo": max(
            min(i["alta"],  f["baja"],  a["baja"]),   # RD5
            min(i["media"], f["media"], a["baja"]),   # RD6
            min(i["media"], f["baja"],  a["media"]),  # RD7
            min(i["media"], f["media"], a["media"]),  # RD8
            # Nuevas (RD16-RD23): combinaciones con una o dos presiones elevadas
            min(i["baja"],  f["media"], a["alta"]),   # RD16: B+M+A
            min(i["baja"],  f["alta"],  a["media"]),  # RD17: B+A+M
            min(i["baja"],  f["alta"],  a["alta"]),   # RD18: B+A+A
            min(i["media"], f["baja"],  a["alta"]),   # RD19: M+B+A
            min(i["media"], f["media"], a["alta"]),   # RD20: M+M+A
            min(i["media"], f["alta"],  a["baja"]),   # RD21: M+A+B
            min(i["media"], f["alta"],  a["media"]),  # RD22: M+A+M
            min(i["alta"],  f["baja"],  a["media"]),  # RD23: A+B+M
        ),

        # ── CRÍTICO ──────────────────────────────────────────────────────────
        "critico": max(
            min(i["alta"],  f["media"], a["baja"]),   # RD9
            min(i["alta"],  f["alta"],  a["media"]),  # RD10
            min(i["alta"],  f["alta"],  a["alta"]),   # RD11
            min(i["media"], f["alta"],  a["alta"]),   # RD12
            # Nuevas (RD24-RD27): ingresos altos con presión adicional
            min(i["alta"],  f["baja"],  a["alta"]),   # RD24: A+B+A
            min(i["alta"],  f["media"], a["media"]),  # RD25: A+M+M
            min(i["alta"],  f["media"], a["alta"]),   # RD26: A+M+A  ← corrige bug Case 4
            min(i["alta"],  f["alta"],  a["baja"]),   # RD27: A+A+B
        ),
    }

    return activaciones


def defuzzificar(activaciones):
    """
    PASO 3 — Defuzzificación por método del centroide (centro de gravedad).
    
    Convierte los grados de activación de los conjuntos de salida
    en un único valor numérico entre 0 y 100.
    
    El método del centroide calcula el promedio ponderado de todos los
    puntos del universo de discurso (0 a 100), donde el peso de cada
    punto es el grado de pertenencia al conjunto difuso de salida
    recortado por su activación (método de Mamdani: min entre la
    función de membresía y el grado de activación).
    
    Retorna:
        float — valor numérico del riesgo fiscal (0 a 100)
    """
    # Crear el universo de discurso: 1000 puntos entre 0 y 100
    universo = np.linspace(0, 100, 1000)

    # Para cada punto del universo, calcular su grado de pertenencia
    # al conjunto de salida resultante (recortado por la activación de cada regla)
    membresía_total = np.zeros(len(universo))

    for x in range(len(universo)):
        val = universo[x]
        # Método Mamdani: recortar cada función de membresía con su activación
        grado_estable    = min(activaciones["estable"],    riesgo_estable(val))
        grado_precaucion = min(activaciones["precaucion"], riesgo_precaucion(val))
        grado_riesgo     = min(activaciones["riesgo"],     riesgo_zona_riesgo(val))
        grado_critico    = min(activaciones["critico"],    riesgo_critico(val))
        # Combinar con OR = máximo
        membresía_total[x] = max(grado_estable, grado_precaucion, grado_riesgo, grado_critico)

    # Centroide: suma(x * membresía(x)) / suma(membresía(x))
    suma_pesos = np.sum(membresía_total)
    if suma_pesos == 0:
        return 0.0  # Si no hay activación, riesgo nulo

    centroide = np.sum(universo * membresía_total) / suma_pesos
    return round(float(centroide), 2)


def interpretar_riesgo(valor_numerico):
    """
    Convierte el valor numérico del centroide (0-100) a una etiqueta lingüística.
    
    Rangos:
        0-25  → Situación Estable
        26-50 → Zona de Precaución
        51-75 → Zona de Riesgo
        76-100 → Zona Crítica
    """
    if valor_numerico <= 25:
        return "SITUACIÓN ESTABLE"
    elif valor_numerico <= 50:
        return "ZONA DE PRECAUCIÓN"
    elif valor_numerico <= 75:
        return "ZONA DE RIESGO"
    else:
        return "ZONA CRÍTICA"


def evaluar_riesgo_difuso(categoria_final, ingresos, superficie, energia, alquiler):
    """
    Función principal del módulo difuso. Orquesta los tres pasos:
    fuzzificación → inferencia → defuzzificación.
    
    Parámetros:
        categoria_final : str — categoría ajustada
        ingresos        : float
        superficie      : float
        energia         : float
        alquiler        : float
    
    Retorna:
        dict con presiones, grados, activaciones, valor numérico y etiqueta
    """
    # Paso 0: calcular presiones
    presiones = calcular_presiones(categoria_final, ingresos, superficie, energia, alquiler)

    # Paso 1: fuzzificar
    grados = fuzzificar(
        presiones["presion_ingresos"],
        presiones["presion_fisica"],
        presiones["presion_alquiler"]
    )

    # Paso 2: aplicar reglas difusas
    activaciones = aplicar_reglas_difusas(grados)

    # Paso 3: defuzzificar
    valor_numerico = defuzzificar(activaciones)

    # Interpretar resultado
    etiqueta = interpretar_riesgo(valor_numerico)

    return {
        "presiones":       presiones,
        "grados":          grados,
        "activaciones":    activaciones,
        "valor_numerico":  valor_numerico,
        "etiqueta":        etiqueta
    }