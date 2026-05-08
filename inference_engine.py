# =============================================================================
# inference_engine.py — Motor de Inferencia Determinístico
# =============================================================================
# Este módulo implementa el encadenamiento hacia adelante (forward chaining)
# para los Bloques 1 al 4 de la base de conocimiento.
#
# El razonamiento sigue tres etapas en orden:
#   1. Determinar la categoría base según ingresos y tipo de actividad
#   2. Ajustar la categoría si los parámetros físicos lo requieren
#   3. Detectar alertas de exclusión determinísticas
#
# Cada función devuelve un diccionario con:
#   - El resultado de la inferencia
#   - Las reglas que se activaron (subsistema de explicación)
# =============================================================================

from knowledge_base import CATEGORIAS, ORDEN_CATEGORIAS, PRECIO_UNITARIO_MAX, INGRESO_MAX_REGIMEN


def determinar_categoria_por_ingresos(actividad, ingresos):
    """
    BLOQUE 1 y 2 — Asignación de categoría por ingresos.
    
    Aplica las reglas R1-R24 según el tipo de actividad.
    Recorre las categorías de menor a mayor y asigna la primera
    cuyo límite de ingresos supere el valor declarado.
    
    Parámetros:
        actividad : str — "servicios" o "venta"
        ingresos  : float — ingresos brutos anuales en pesos
    
    Retorna:
        dict con 'categoria', 'regla_activada', 'cf', 'explicacion'
    """
    reglas_activadas = []

    # Verificar primero si supera el límite máximo del régimen (R12 / R24)
    if ingresos > INGRESO_MAX_REGIMEN:
        regla = "R12" if actividad == "servicios" else "R24"
        return {
            "categoria": None,
            "regla_activada": regla,
            "cf": 1.0,
            "explicacion": (
                f"[{regla}] Los ingresos anuales (${ingresos:,.2f}) superan el límite "
                f"máximo del régimen (${INGRESO_MAX_REGIMEN:,.2f}). "
                f"El contribuyente debe pasar al Régimen General."
            )
        }

    # Recorrer categorías de A a K y asignar la que corresponde según ingresos
    for i, cat in enumerate(ORDEN_CATEGORIAS):
        limite = CATEGORIAS[cat]["ingreso_max"]
        if ingresos <= limite:
            # Calcular número de regla según bloque (Bloque 1: R1-R11, Bloque 2: R13-R23)
            num_regla = i + 1 if actividad == "servicios" else i + 13
            regla = f"R{num_regla}"
            return {
                "categoria": cat,
                "regla_activada": regla,
                "cf": 1.0,
                "explicacion": (
                    f"[{regla}] Actividad: {actividad}. "
                    f"Ingresos anuales: ${ingresos:,.2f}. "
                    f"Límite de categoría {cat}: ${limite:,.2f}. "
                    f"→ Categoría asignada por ingresos: {cat} (CF=1.0)"
                )
            }

    # Si llegó hasta acá sin asignar, es exclusión
    return {
        "categoria": None,
        "regla_activada": "R12/R24",
        "cf": 1.0,
        "explicacion": "Ingresos superan el límite máximo. Debe pasar al Régimen General."
    }


def ajustar_por_parametros_fisicos(categoria_base, superficie, energia):
    """
    BLOQUE 3 — Recategorización por parámetros físicos.
    
    Aplica las reglas R25-R36. Verifica si la superficie o la energía
    consumida superan los límites de la categoría base y, de ser así,
    sube la categoría a la siguiente que admita esos valores.
    
    Parámetros:
        categoria_base : str — categoría determinada por ingresos (ej: "C")
        superficie     : float — superficie afectada en m²
        energia        : float — energía consumida anual en kWh
    
    Retorna:
        dict con 'categoria_final', 'reglas_activadas', 'explicacion'
    """
    reglas_activadas = []
    explicaciones = []
    categoria_actual = categoria_base
    idx_actual = ORDEN_CATEGORIAS.index(categoria_base)

    # --- Verificar superficie ---
    # Recorre desde la categoría base hacia arriba buscando la que admita la superficie
    for i in range(idx_actual, len(ORDEN_CATEGORIAS)):
        cat = ORDEN_CATEGORIAS[i]
        if superficie <= CATEGORIAS[cat]["superficie_max"]:
            if cat != categoria_base:
                # Calcular número de regla (R25 a R30 para superficie)
                num_regla = 25 + (idx_actual)
                regla = f"R{num_regla}"
                reglas_activadas.append(regla)
                explicaciones.append(
                    f"[{regla}] Superficie ({superficie} m²) supera el límite de "
                    f"categoría {categoria_base} ({CATEGORIAS[categoria_base]['superficie_max']} m²). "
                    f"→ Recategorizado a {cat} por superficie."
                )
                categoria_actual = cat
            break

    # --- Verificar energía ---
    idx_actual_energia = ORDEN_CATEGORIAS.index(categoria_actual)
    for i in range(idx_actual_energia, len(ORDEN_CATEGORIAS)):
        cat = ORDEN_CATEGORIAS[i]
        if energia <= CATEGORIAS[cat]["energia_max"]:
            if cat != categoria_actual:
                num_regla = 31 + (idx_actual_energia)
                regla = f"R{num_regla}"
                reglas_activadas.append(regla)
                explicaciones.append(
                    f"[{regla}] Energía consumida ({energia} kWh) supera el límite de "
                    f"categoría {categoria_actual} ({CATEGORIAS[categoria_actual]['energia_max']} kWh). "
                    f"→ Recategorizado a {cat} por energía."
                )
                categoria_actual = cat
            break

    # Si no hubo cambios, informar que los parámetros físicos son coherentes
    if not reglas_activadas:
        explicaciones.append(
            f"Superficie ({superficie} m²) y energía ({energia} kWh) "
            f"son coherentes con categoría {categoria_base}. No se requiere ajuste."
        )

    return {
        "categoria_final": categoria_actual,
        "reglas_activadas": reglas_activadas,
        "explicacion": " | ".join(explicaciones)
    }


def detectar_alertas(categoria_final, actividad, ingresos, alquiler, precio_unitario):
    """
    BLOQUE 4 — Alertas determinísticas de exclusión.
    
    Aplica las reglas R37-R43. Detecta situaciones donde la normativa
    establece que el contribuyente enfrenta riesgo de exclusión del régimen.
    
    Parámetros:
        categoria_final  : str — categoría ya ajustada por parámetros físicos
        actividad        : str — "servicios" o "venta"
        ingresos         : float — ingresos brutos anuales
        alquiler         : float — alquiler devengado anual en pesos
        precio_unitario  : float — precio unitario máximo de venta (solo para venta)
    
    Retorna:
        list de dicts, cada uno con 'regla', 'cf', 'tipo_alerta', 'explicacion'
    """
    alertas = []

    # R37 — Precio unitario máximo (solo para venta de cosas muebles)
    if actividad == "venta" and precio_unitario > PRECIO_UNITARIO_MAX:
        alertas.append({
            "regla": "R37",
            "cf": 0.9,
            "tipo_alerta": "PRECIO UNITARIO EXCEDIDO",
            "explicacion": (
                f"[R37] El precio unitario máximo declarado (${precio_unitario:,.2f}) "
                f"supera el límite permitido (${PRECIO_UNITARIO_MAX:,.2f}). "
                f"Riesgo de exclusión del régimen. (CF=0.9)"
            )
        })

    # R38-R42 — Alquiler devengado según categoría
    if categoria_final is not None:
        limite_alquiler = CATEGORIAS[categoria_final]["alquiler_max"]
        if alquiler > limite_alquiler:
            # Determinar número de regla según categoría
            reglas_alquiler = {
                "A": "R38", "B": "R38",
                "C": "R39", "D": "R39",
                "E": "R40", "F": "R40",
                "G": "R41",
                "H": "R42", "I": "R42", "J": "R42", "K": "R42"
            }
            regla = reglas_alquiler.get(categoria_final, "R38")
            alertas.append({
                "regla": regla,
                "cf": 1.0,
                "tipo_alerta": "ALQUILER EXCEDIDO",
                "explicacion": (
                    f"[{regla}] Alquiler devengado anual (${alquiler:,.2f}) supera el "
                    f"límite permitido para categoría {categoria_final} "
                    f"(${limite_alquiler:,.2f}). Exclusión del régimen. (CF=1.0)"
                )
            })

    # R43 — Exclusión por ingresos que superan el máximo del régimen
    if ingresos > INGRESO_MAX_REGIMEN:
        alertas.append({
            "regla": "R43",
            "cf": 1.0,
            "tipo_alerta": "EXCLUSIÓN RÉGIMEN GENERAL",
            "explicacion": (
                f"[R43] Ingresos anuales (${ingresos:,.2f}) superan el límite máximo "
                f"del Monotributo (${INGRESO_MAX_REGIMEN:,.2f}). "
                f"Debe pasar al Régimen General de forma obligatoria. (CF=1.0)"
            )
        })

    return alertas