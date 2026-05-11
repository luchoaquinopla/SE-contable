# =============================================================================
# presenter.py — Subsistema de Explicación (Capa de Presentación)
# =============================================================================
# Responsabilidad única: formatear y mostrar en consola el diagnóstico
# producido por expert_system.py. Se separa de la orquestación para que
# cambios en el formato de salida (consola, JSON, HTML) no toquen la lógica
# del sistema experto.
# =============================================================================


def mostrar_resultado(resultado):
    """
    Imprime el diagnóstico completo del sistema experto de forma estructurada,
    incluyendo categoría, alertas, nivel de riesgo y reglas activadas.
    """
    sep = "=" * 65

    print(f"\n{sep}")
    print(f"  SISTEMA EXPERTO DE MONOTRIBUTO — {resultado['nombre'].upper()}")
    print(sep)

    # --- Diagnóstico principal ---
    print(f"\n  📋 DIAGNÓSTICO")
    if resultado["categoria_base"] is not None:
        print(f"  Categoría por ingresos : {resultado['categoria_base']}")
    print(f"  Categoría final        : {resultado['categoria_final']}")

    if resultado["exclusion"] or resultado["categoria_final"] == "EXCLUIDO":
        print(f"  Impuesto mensual       : N/A (excluido del régimen)")
        print(f"\n  ⚠️  El contribuyente debe pasar al RÉGIMEN GENERAL (IVA + Ganancias).")
    elif resultado.get("desglose_mensual"):
        d = resultado["desglose_mensual"]
        print(f"\n  💰 OBLIGACIÓN MENSUAL (desglose)")
        print(f"  Impuesto integrado     : ${d['impuesto_integrado']:>12,.2f}")
        print(f"  Aportes SIPA           : ${d['sipa']:>12,.2f}")
        print(f"  Obra social            : ${d['obra_social']:>12,.2f}")
        print(f"  {'─' * 39}")
        print(f"  TOTAL MENSUAL          : ${d['total']:>12,.2f}")

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
