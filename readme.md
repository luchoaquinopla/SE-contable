# Sistema Experto de Categorización de Monotributo

**Asignatura:** Sistemas Inteligentes — Práctica de Laboratorio N° 9  
**Carrera:** Ingeniería en Sistemas de Información  
**Normativa base:** ARCA (ex AFIP) — Vigente desde 01/02/2026

---

## ¿Qué hace este sistema?

Este programa es un **Sistema Experto híbrido** que asesora a contribuyentes inscriptos (o que quieren inscribirse) en el **Régimen Simplificado para Pequeños Contribuyentes (Monotributo)** de Argentina.

Dado un conjunto de datos del contribuyente, el sistema determina:

1. **Qué categoría de Monotributo le corresponde** (de la A a la K), según sus ingresos, tipo de actividad y parámetros físicos.
2. **Si existen alertas de exclusión del régimen** (alquiler excedido, precio unitario excedido, superficie o energía que superan los límites absolutos del régimen, ingresos fuera del régimen).
3. **Cuál es su nivel de riesgo fiscal global** (Situación Estable / Zona de Precaución / Zona de Riesgo / Zona Crítica), usando lógica difusa para capturar la gradualidad del razonamiento contable.
4. **Por qué llegó a esa conclusión**, mostrando exactamente qué reglas se activaron (subsistema de explicación).

---

## Requisitos

- Python 3.8 o superior
- Librería `numpy`

### Instalación de dependencias

```bash
pip install numpy
```

---

## Cómo ejecutar el sistema

```bash
python main.py
```

Al ejecutarlo, aparece un menú con tres opciones:

```
[1] Ingresar datos de un contribuyente (modo interactivo)
[2] Ejecutar todos los casos de prueba
[3] Ejecutar un caso de prueba específico
```

---

## Estructura del proyecto

```
se_monotributo/
│
├── main.py               # Punto de entrada. Menú y modos de uso.
├── knowledge_base.py     # Datos normativos: tablas ARCA, límites y constantes.
├── fuzzy_membership.py   # Funciones de membresía difusa (trapezoidal/triangular).
├── inference_engine.py   # Motor determinístico: reglas R1–R50 (Bloques 1 a 4).
├── fuzzy_engine.py       # Motor difuso: fuzzificación → inferencia → defuzzificación (Bloque 5).
├── expert_system.py      # Orquestador: coordina los módulos y produce el diagnóstico.
├── presenter.py          # Presentación: formatea y muestra el diagnóstico en consola.
├── test_cases.py         # Los 9 casos de prueba predefinidos.
└── README.md             # Este archivo.
```

---

## Descripción de cada archivo

### `knowledge_base.py` — Datos Normativos

Responsabilidad única: **almacenar los datos normativos del régimen**. Es el único archivo que debe modificarse si ARCA actualiza sus tablas. No contiene ninguna función computacional.

- `CATEGORIAS`: diccionario con los límites de ingreso, superficie, energía y alquiler de cada categoría (A a K), más el impuesto integrado mensual por tipo de actividad.
- `ORDEN_CATEGORIAS`: lista ordenada de categorías, usada para la lógica de recategorización.
- `PRECIO_UNITARIO_MAX`, `INGRESO_MAX_REGIMEN`, `ALQUILER_MAX_GLOBAL`: constantes del régimen.

### `fuzzy_membership.py` — Funciones de Membresía

Responsabilidad única: **definir la matemática del módulo difuso**. Se separa de `knowledge_base.py` porque son dos razones de cambio distintas: si AFIP actualiza sus valores, este archivo no cambia; si se ajusta el modelo difuso, `knowledge_base.py` no cambia.

- `membresia_trapezoidal()` y `membresia_triangular()`: funciones de forma genéricas.
- `presion_baja()`, `presion_media()`, `presion_alta()`: conjuntos difusos de entrada.
- `riesgo_estable()`, `riesgo_precaucion()`, `riesgo_zona_riesgo()`, `riesgo_critico()`: conjuntos difusos de salida.

### `inference_engine.py` — Motor de Inferencia Determinístico

Implementa el **encadenamiento hacia adelante** para los cuatro bloques de reglas determinísticas:

| Función | Bloque | Reglas | Qué hace |
|---|---|---|---|
| `determinar_categoria_por_ingresos()` | 1 y 2 | R1–R24 | Asigna categoría base según ingresos y actividad |
| `ajustar_por_parametros_fisicos()` | 3 | R25–R36 | Sube la categoría si superficie o energía lo requieren |
| `ajustar_por_empleados()` | 3 (ext.) | R48–R50 | Aplica el piso de categoría mínimo por empleados en relación de dependencia |
| `detectar_alertas()` | 4 | R37–R47 | Detecta alertas de exclusión por alquiler, precio unitario, superficie o energía |

Cada función devuelve un diccionario con el resultado y las reglas activadas, que alimentan el subsistema de explicación.

### `fuzzy_engine.py` — Motor de Lógica Difusa

Implementa el **Bloque 5** en tres pasos secuenciales:

| Función | Paso | Qué hace |
|---|---|---|
| `calcular_presiones()` | Previo | Calcula los tres porcentajes de presión (ingresos, física, alquiler) |
| `fuzzificar()` | 1 — Fuzzificación | Convierte las presiones en grados de pertenencia (baja/media/alta) |
| `aplicar_reglas_difusas()` | 2 — Inferencia | Aplica las 27 reglas difusas (RD1–RD27) con AND=mínimo, OR=máximo |
| `defuzzificar()` | 3 — Defuzzificación | Aplica el método del centroide para obtener el valor numérico 0–100 |
| `interpretar_riesgo()` | Post | Convierte el valor numérico en etiqueta lingüística |
| `evaluar_riesgo_difuso()` | Orquestador | Llama a todas las anteriores en orden |

### `expert_system.py` — Orquestador

Responsabilidad única: **coordinar los módulos en el orden correcto** y devolver el diagnóstico como un diccionario. No contiene lógica de presentación. La función principal `ejecutar_sistema_experto(caso)` recibe los datos del contribuyente y ejecuta cuatro etapas: categoría por ingresos → ajuste físico → piso por empleados → alertas → evaluación difusa.

### `presenter.py` — Presentación

Responsabilidad única: **formatear y mostrar en consola** el diagnóstico producido por `expert_system.py`. Se separa del orquestador para que cualquier cambio en el formato de salida (consola, JSON, archivo de log) no afecte la lógica del sistema experto.

- `mostrar_resultado(resultado)`: imprime categoría, alertas, nivel de riesgo, presiones calculadas y reglas activadas.

### `test_cases.py` — Casos de Prueba

Contiene los 10 casos de prueba predefinidos. Cada caso es un diccionario con las entradas del contribuyente. Los casos cubren todos los escenarios del sistema:

| Caso | Escenario | Qué valida |
|---|---|---|
| Caso 1 | Diseñador gráfico, categoría A | Caso simple, situación estable |
| Caso 2 | Contador con oficina grande | Recategorización por superficie (R26) |
| Caso 3 | Comerciante de ropa, ingresos altos | Zona crítica por presión combinada |
| Caso 4 | Odontóloga con alquiler caro | Exclusión por alquiler (R39) |
| Caso 5 | Vendedor de electrónica | Exclusión por precio unitario (R47) |
| Caso 6 | Médico de altos ingresos | Exclusión total del régimen (R12) |
| Caso 7 ⚠️ | Electricista al 91% del límite | Caso límite — gradualidad del módulo difuso |
| Caso 8 | Local con 250 m² | Exclusión por superficie (R44) |
| Caso 9 | Taller con 25.000 kWh | Exclusión por energía (R45) |
| Caso 10 | Kiosquero con 1 empleado | Piso de categoría por empleados (R48) |

### `main.py` — Punto de Entrada

Gestiona los dos modos de uso del sistema: interactivo (el usuario ingresa datos por consola) y automático (ejecuta los casos de prueba predefinidos). No contiene lógica del SE.

---

## Flujo del sistema

```
Datos del contribuyente
        │
        ▼
[inference_engine] Bloques 1/2 — ¿Qué categoría por ingresos? (R1–R24)
        │
        ▼
[inference_engine] Bloque 3 — ¿Hay que recategorizar por parámetros físicos? (R25–R36)
        │
        ▼
[inference_engine] Bloque 3 ext. — ¿Hay piso de categoría por empleados? (R48–R50)
        │
        ▼
[inference_engine] Bloque 4 — ¿Hay alertas de exclusión? (R37–R47)
        │
        ▼
[fuzzy_engine] Bloque 5 — ¿Cuál es el riesgo fiscal global?
  calcular_presiones → fuzzificar → aplicar_reglas_difusas (RD1–RD27) → defuzzificar
        │
        ▼
[expert_system] Diagnóstico unificado (dict con reglas activadas)
        │
        ▼
[presenter] Salida formateada en consola
```

---

## Dependencias entre módulos

```
main.py
  ├── expert_system.py
  │     ├── inference_engine.py
  │     │     └── knowledge_base.py
  │     ├── fuzzy_engine.py
  │     │     ├── knowledge_base.py
  │     │     └── fuzzy_membership.py
  │     └── knowledge_base.py
  ├── presenter.py          (sin dependencias del proyecto)
  └── test_cases.py         (sin dependencias del proyecto)
```

---

## Ejemplo de salida

```
=================================================================
  SISTEMA EXPERTO DE MONOTRIBUTO — CASO 7 (LÍMITE)
=================================================================

  📋 DIAGNÓSTICO
  Categoría por ingresos : B
  Categoría final        : B
  Impuesto mensual       : $     9,082.88

  🎯 RIESGO FISCAL GLOBAL (Módulo Difuso)
  Valor numérico : 58.1 / 100
  Etiqueta       : ZONA DE RIESGO

  Presiones calculadas:
    Presión de ingresos  : 91.0%
    Presión física       : 64.0%
    Presión de alquiler  : 37.6%

  📖 ¿POR QUÉ LLEGÓ A ESTA CONCLUSIÓN? (Reglas activadas)
  Reglas: R2, RD5, RD6, RD7, RD8

  1. [R2] Ingresos $13,703,187 dentro del límite de Cat. B ($15,058,447). CF=1.0
  2. Superficie y energía coherentes con categoría B.
```

---

## Notas importantes

- Los valores normativos están **actualizados a la tabla vigente desde 01/02/2026** publicada por ARCA.
- El parámetro de superficie **no aplica en localidades de menos de 40.000 habitantes**, según la normativa. El sistema asume que el contribuyente está en una localidad donde aplica.
- El sistema es una herramienta de orientación. Para decisiones impositivas definitivas, consultar siempre a un contador público matriculado.
