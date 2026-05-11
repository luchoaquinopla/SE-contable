
from inference_engine import (
    determinar_categoria_por_ingresos,
    ajustar_por_parametros_fisicos,
    ajustar_por_empleados,
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
    # MÓDULO 1 — PASO 2b: Ajustar categoría por piso de empleados
    # =========================================================================
    resultado_empleados = ajustar_por_empleados(categoria_final, empleados)
    if resultado_empleados["regla_activada"]:
        reglas_activadas.append(resultado_empleados["regla_activada"])
        explicaciones.append(resultado_empleados["explicacion"])
        categoria_final = resultado_empleados["categoria_final"]

    # =========================================================================
    # MÓDULO 1 — PASO 3: Detectar alertas determinísticas de exclusión
    # =========================================================================
    alertas = detectar_alertas(categoria_final, actividad, ingresos, superficie, energia, alquiler, precio_unit)
    for alerta in alertas:
        reglas_activadas.append(alerta["regla"])
        explicaciones.append(alerta["explicacion"])

    # Reglas que implican exclusión obligatoria del régimen (CF = 1.0)
    REGLAS_EXCLUSION_DURA = {"R38", "R39", "R40", "R41", "R42", "R44", "R45", "R46", "R47"}
    hay_exclusion_dura = any(a["regla"] in REGLAS_EXCLUSION_DURA for a in alertas)

    # Cuando la exclusión es por causa no física (ej: alquiler), el mensaje
    # "parámetros físicos coherentes" no aporta y puede confundir — se suprime.
    if hay_exclusion_dura and len(explicaciones) > 1 and "coherentes con categoría" in explicaciones[1]:
        explicaciones.pop(1)

    # categoria_calculo se usa para el módulo difuso (presiones reales, aunque haya exclusión)
    # categoria_display es lo que se muestra en el diagnóstico
    categoria_calculo = categoria_final
    categoria_display = "EXCLUIDO" if hay_exclusion_dura else categoria_final

    # =========================================================================
    # MÓDULO 2 — Evaluación de riesgo fiscal global (lógica difusa)
    # =========================================================================
    resultado_difuso = evaluar_riesgo_difuso(
        categoria_calculo, ingresos, superficie, energia, alquiler
    )
    reglas_difusas_activadas = _identificar_reglas_difusas(resultado_difuso["activaciones"])
    reglas_activadas.extend(reglas_difusas_activadas)

    # Desglose de obligaciones mensuales: N/A si hay exclusión del régimen
    if hay_exclusion_dura:
        desglose = None
    else:
        cat_data = CATEGORIAS[categoria_final]
        imp_integrado = cat_data["impuesto_servicios" if actividad == "servicios" else "impuesto_venta"]
        sipa = cat_data["sipa"]
        obra_social = cat_data["obra_social"]
        desglose = {
            "impuesto_integrado": imp_integrado,
            "sipa":               sipa,
            "obra_social":        obra_social,
            "total":              imp_integrado + sipa + obra_social,
        }

    return {
        "nombre":           caso["nombre"],
        "categoria_base":   categoria_base,
        "categoria_final":  categoria_display,
        "alertas":          alertas,
        "riesgo_numerico":  resultado_difuso["valor_numerico"],
        "riesgo_etiqueta":  resultado_difuso["etiqueta"],
        "presiones":        resultado_difuso["presiones"],
        "activaciones":     resultado_difuso["activaciones"],
        "reglas_activadas": reglas_activadas,
        "explicaciones":    explicaciones,
        "desglose_mensual": desglose,
        "impuesto_mensual": desglose["total"] if desglose else None,
        "exclusion":        hay_exclusion_dura
    }


def _armar_resultado_exclusion(caso, reglas_activadas, explicaciones):
    """
    Construye el resultado cuando el contribuyente está fuera del régimen.
    Se llama cuando los ingresos superan el límite máximo del Monotributo.
    """
    return {
        "nombre":           caso["nombre"],
        "categoria_base":   None,
        "categoria_final":  "EXCLUIDO",
        "alertas":          [{"regla": "R43", "tipo_alerta": "EXCLUSIÓN RÉGIMEN GENERAL", "cf": 1.0}],
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
        "precaucion": ["RD2", "RD3", "RD4", "RD13", "RD14", "RD15"],
        "riesgo":     ["RD5", "RD6", "RD7", "RD8", "RD16", "RD17", "RD18", "RD19", "RD20", "RD21", "RD22", "RD23"],
        "critico":    ["RD9", "RD10", "RD11", "RD12", "RD24", "RD25", "RD26", "RD27"]
    }
    activadas = []
    for conjunto, reglas in mapeo.items():
        if activaciones.get(conjunto, 0) > 0:
            activadas.extend(reglas)
    return activadas
