# =============================================================================
# expert_system.py — Sistema Experto de Monotributo (Módulo Principal)
# =============================================================================
# Este es el módulo central que integra los tres módulos del sistema:
#
#   1. inference_engine.py → reglas determinísticas (Bloques 1-4)
#   2. fuzzy_engine.py     → lógica difusa (Bloque 5)
#   3. knowledge_base.py   → datos normativos y funciones de membresía
#
# Flujo del sistema:
#   Datos del contribuyente
#       → Módulo 1: determinar categoría por ingresos
#       → Módulo 1: ajustar por parámetros físicos
#       → Módulo 1: detectar alertas de exclusión
#       → Módulo 2: evaluar riesgo fiscal global (lógica difusa)
#       → Subsistema de explicación: mostrar reglas activadas y conclusión
# =============================================================================

from inference_engine import (
    determinar_categoria_por_ingresos,
    ajustar_por_parametros_fisicos,
    detectar_alertas
)
from fuzzy_engine import evaluar_riesgo_difuso
from knowledge_base import CATEGORIAS


def ejecutar_sistema_experto(caso):
    """
    Función principal del SE. Recibe un caso y devuelve el diagnóstico completo.
    
    Parámetros:
        caso : dict con las siguientes claves:
            - nombre        : str  — identificador del caso (ej: "Caso 1")
            - actividad     : str  — "servicios" o "venta"
            - ingresos      : float — ingresos brutos anuales en pesos
            - superficie    : float — superficie afectada en m²
            - energia       : float — energía eléctrica consumida anual en kWh
            - alquiler      : float — alquiler devengado anual en pesos
            - precio_unit   : float — precio unitario máximo (solo para venta)
            - empleados     : int   — cantidad de empleados en relación de dependencia
    
    Retorna:
        dict con el diagnóstico completo y todas las reglas activadas
    """
    actividad    = caso["actividad"]
    ingresos     = caso["ingresos"]
    superficie   = caso["superficie"]
    energia      = caso["energia"]
    alquiler     = caso["alquiler"]
    precio_unit  = caso.get("precio_unit", 0)
    empleados    = caso.get("empleados", 0)

    reglas_activadas = []
    explicaciones    = []

    # =========================================================================
    # MÓDULO 1 — PASO 1: Determinar categoría base por ingresos
    # =========================================================================
    resultado_ingresos = determinar_categoria_por_ingresos(actividad, ingresos)
    reglas_activadas.append(resultado_ingresos["regla_activada"])
    explicaciones.append(resultado_ingresos["explicacion"])
    categoria_base = resultado_ingresos["categoria"]

    # Si hay exclusión por ingresos, detener el proceso
    if categoria_base is None:
        return _armar_resultado_exclusion(caso, reglas_activadas, explicaciones)

    # =========================================================================
    # MÓDULO 1 — PASO 2: Ajustar categoría por parámetros físicos
    # =========================================================================
    resultado_fisico = ajustar_por_parametros_fisicos(categoria_base, superficie, energia)
    reglas_activadas.extend(resultado_fisico["reglas_activadas"])
    explicaciones.append(resultado_fisico["explicacion"])
    categoria_final = resultado_fisico["categoria_final"]

    # =========================================================================
    # MÓDULO 1 — PASO 3: Detectar alertas determinísticas de exclusión
    # =========================================================================
    alertas = detectar_alertas(categoria_final, actividad, ingresos, alquiler, precio_unit)
    for alerta in alertas:
        reglas_activadas.append(alerta["regla"])
        explicaciones.append(alerta["explicacion"])

    # =========================================================================
    # MÓDULO 2 — Evaluación de riesgo fiscal global (lógica difusa)
    # =========================================================================
    resultado_difuso = evaluar_riesgo_difuso(
        categoria_final, ingresos, superficie, energia, alquiler
    )
    reglas_difusas_activadas = _identificar_reglas_difusas(resultado_difuso["activaciones"])
    reglas_activadas.extend(reglas_difusas_activadas)

    # Obtener impuesto integrado mensual
    impuesto = CATEGORIAS[categoria_final][
        "impuesto_servicios" if actividad == "servicios" else "impuesto_venta"
    ]

    return {
        "nombre":           caso["nombre"],
        "categoria_base":   categoria_base,
        "categoria_final":  categoria_final,
        "alertas":          alertas,
        "riesgo_numerico":  resultado_difuso["valor_numerico"],
        "riesgo_etiqueta":  resultado_difuso["etiqueta"],
        "presiones":        resultado_difuso["presiones"],
        "activaciones":     resultado_difuso["activaciones"],
        "reglas_activadas": reglas_activadas,
        "explicaciones":    explicaciones,
        "impuesto_mensual": impuesto,
        "exclusion":        False
    }


def _armar_resultado_exclusion(caso, reglas_activadas, explicaciones):
    """
    Construye el resultado cuando el contribuyente está fuera del régimen.
    Se llama cuando los ingresos superan el límite máximo del Monotributo.
    """
    return {
        "nombre":           caso["nombre"],
        "categoria_base":   None,
        "categoria_final":  None,
        "alertas":          [{"tipo_alerta": "EXCLUSIÓN RÉGIMEN GENERAL", "cf": 1.0}],
        "riesgo_numerico":  100.0,
        "riesgo_etiqueta":  "ZONA CRÍTICA — EXCLUSIÓN DEL RÉGIMEN",
        "presiones":        {"presion_ingresos": 1.0, "presion_fisica": 1.0, "presion_alquiler": 1.0},
        "activaciones":     {},
        "reglas_activadas": reglas_activadas,
        "explicaciones":    explicaciones,
        "impuesto_mensual": None,
        "exclusion":        True
    }


def _identificar_reglas_difusas(activaciones):
    """
    Identifica qué reglas difusas (RD1-RD12) se activaron con grado > 0.
    Se usa para el subsistema de explicación.
    """
    mapeo = {
        "estable":    ["RD1"],
        "precaucion": ["RD2", "RD3", "RD4"],
        "riesgo":     ["RD5", "RD6", "RD7", "RD8"],
        "critico":    ["RD9", "RD10", "RD11", "RD12"]
    }
    activadas = []
    for conjunto, reglas in mapeo.items():
        if activaciones.get(conjunto, 0) > 0:
            activadas.extend(reglas)
    return activadas


def mostrar_resultado(resultado):
    """
    Subsistema de explicación: imprime el diagnóstico completo en consola
    de forma clara y estructurada, incluyendo todas las reglas activadas.
    """
    sep = "=" * 65

    print(f"\n{sep}")
    print(f"  SISTEMA EXPERTO DE MONOTRIBUTO — {resultado['nombre'].upper()}")
    print(sep)

    # --- Diagnóstico principal ---
    if resultado["exclusion"]:
        print(f"\n  ⚠️  EXCLUSIÓN DEL MONOTRIBUTO")
        print(f"  El contribuyente debe pasar al RÉGIMEN GENERAL (IVA + Ganancias).")
    else:
        print(f"\n  📋 DIAGNÓSTICO")
        print(f"  Categoría por ingresos : {resultado['categoria_base']}")
        print(f"  Categoría final        : {resultado['categoria_final']}")
        print(f"  Impuesto mensual       : ${resultado['impuesto_mensual']:>12,.2f}")

    # --- Alertas ---
    if resultado["alertas"]:
        print(f"\n  ⚠️  ALERTAS DETECTADAS")
        for alerta in resultado["alertas"]:
            print(f"  → {alerta['tipo_alerta']} (CF={alerta.get('cf', 1.0)})")

    # --- Riesgo fiscal (módulo difuso) ---
    print(f"\n  🎯 RIESGO FISCAL GLOBAL (Módulo Difuso)")
    print(f"  Valor numérico : {resultado['riesgo_numerico']:.1f} / 100")
    print(f"  Etiqueta       : {resultado['riesgo_etiqueta']}")

    if resultado["presiones"]:
        p = resultado["presiones"]
        print(f"\n  Presiones calculadas:")
        print(f"    Presión de ingresos  : {p['presion_ingresos']*100:.1f}%")
        print(f"    Presión física       : {p['presion_fisica']*100:.1f}%")
        print(f"    Presión de alquiler  : {p['presion_alquiler']*100:.1f}%")

    # --- Subsistema de explicación ---
    print(f"\n  📖 ¿POR QUÉ LLEGÓ A ESTA CONCLUSIÓN? (Reglas activadas)")
    print(f"  Reglas: {', '.join(resultado['reglas_activadas'])}")
    print()
    for i, exp in enumerate(resultado["explicaciones"], 1):
        print(f"  {i}. {exp}")

    print(f"\n{sep}\n")