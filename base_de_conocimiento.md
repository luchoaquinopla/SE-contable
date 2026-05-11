# Base de Conocimiento — Sistema Experto de Monotributo

**Normativa base:** ARCA (ex AFIP) — Vigente desde 01/02/2026  
**Total de reglas:** 50 determinísticas (R1–R50) + 27 difusas (RD1–RD27)

---

## Bloque 1 — Asignación de categoría por ingresos (Servicios)

Aplica cuando `actividad = servicios`. Recorre de menor a mayor y asigna la primera categoría cuyo límite supere los ingresos declarados. CF = 1.0 en todos los casos.

| N° | Condición | Consecuente |
|---|---|---|
| R1 | `actividad = servicios` AND `ingresos ≤ $10.277.988,13` | Categoría **A** |
| R2 | `actividad = servicios` AND `ingresos > $10.277.988,13` AND `≤ $15.058.447,71` | Categoría **B** |
| R3 | `actividad = servicios` AND `ingresos > $15.058.447,71` AND `≤ $21.113.696,52` | Categoría **C** |
| R4 | `actividad = servicios` AND `ingresos > $21.113.696,52` AND `≤ $26.212.853,42` | Categoría **D** |
| R5 | `actividad = servicios` AND `ingresos > $26.212.853,42` AND `≤ $30.833.964,37` | Categoría **E** |
| R6 | `actividad = servicios` AND `ingresos > $30.833.964,37` AND `≤ $38.642.048,36` | Categoría **F** |
| R7 | `actividad = servicios` AND `ingresos > $38.642.048,36` AND `≤ $46.211.109,37` | Categoría **G** |
| R8 | `actividad = servicios` AND `ingresos > $46.211.109,37` AND `≤ $70.113.407,33` | Categoría **H** |
| R9 | `actividad = servicios` AND `ingresos > $70.113.407,33` AND `≤ $78.479.211,62` | Categoría **I** |
| R10 | `actividad = servicios` AND `ingresos > $78.479.211,62` AND `≤ $89.872.640,30` | Categoría **J** |
| R11 | `actividad = servicios` AND `ingresos > $89.872.640,30` AND `≤ $108.357.084,05` | Categoría **K** |
| R12 | `actividad = servicios` AND `ingresos > $108.357.084,05` | **Exclusión del régimen** |

---

## Bloque 2 — Asignación de categoría por ingresos (Venta de cosas muebles)

Estructura idéntica al Bloque 1. Los límites de ingresos son los mismos pero el impuesto integrado mensual difiere. CF = 1.0 en todos los casos.

| N° | Condición | Consecuente |
|---|---|---|
| R13 | `actividad = venta` AND `ingresos ≤ $10.277.988,13` | Categoría **A** |
| R14 | `actividad = venta` AND `ingresos > $10.277.988,13` AND `≤ $15.058.447,71` | Categoría **B** |
| R15 | `actividad = venta` AND `ingresos > $15.058.447,71` AND `≤ $21.113.696,52` | Categoría **C** |
| R16 | `actividad = venta` AND `ingresos > $21.113.696,52` AND `≤ $26.212.853,42` | Categoría **D** |
| R17 | `actividad = venta` AND `ingresos > $26.212.853,42` AND `≤ $30.833.964,37` | Categoría **E** |
| R18 | `actividad = venta` AND `ingresos > $30.833.964,37` AND `≤ $38.642.048,36` | Categoría **F** |
| R19 | `actividad = venta` AND `ingresos > $38.642.048,36` AND `≤ $46.211.109,37` | Categoría **G** |
| R20 | `actividad = venta` AND `ingresos > $46.211.109,37` AND `≤ $70.113.407,33` | Categoría **H** |
| R21 | `actividad = venta` AND `ingresos > $70.113.407,33` AND `≤ $78.479.211,62` | Categoría **I** |
| R22 | `actividad = venta` AND `ingresos > $78.479.211,62` AND `≤ $89.872.640,30` | Categoría **J** |
| R23 | `actividad = venta` AND `ingresos > $89.872.640,30` AND `≤ $108.357.084,05` | Categoría **K** |
| R24 | `actividad = venta` AND `ingresos > $108.357.084,05` | **Exclusión del régimen** |

---

## Bloque 3 — Recategorización por parámetros físicos

Si la superficie o la energía consumida superan los límites de la categoría asignada por ingresos, el sistema sube la categoría a la siguiente que admita esos valores. CF = 1.0.

> Las reglas R25–R30 aplican al índice de la **categoría base por ingresos**.  
> Las reglas R31–R36 aplican al índice de la **categoría ya ajustada por superficie**.

### Recategorización por superficie

| N° | Condición | Consecuente |
|---|---|---|
| R25 | `categoría_base = A` AND `superficie > 30 m²` | Subir a la categoría mínima que admita la superficie |
| R26 | `categoría_base = B` AND `superficie > 45 m²` | Subir a la categoría mínima que admita la superficie |
| R27 | `categoría_base = C` AND `superficie > 60 m²` | Subir a la categoría mínima que admita la superficie |
| R28 | `categoría_base = D` AND `superficie > 85 m²` | Subir a la categoría mínima que admita la superficie |
| R29 | `categoría_base = E` AND `superficie > 110 m²` | Subir a la categoría mínima que admita la superficie |
| R30 | `categoría_base = F` AND `superficie > 150 m²` | Subir a la categoría mínima que admita la superficie |

> Las categorías G–K tienen el mismo límite máximo absoluto de 200 m². Si la superficie supera ese valor, no existe categoría que la admita y se genera la alerta R44.

### Recategorización por energía eléctrica

| N° | Condición | Consecuente |
|---|---|---|
| R31 | `categoría_actual = A` AND `energia > 3.330 kWh` | Subir a la categoría mínima que admita el consumo |
| R32 | `categoría_actual = B` AND `energia > 5.000 kWh` | Subir a la categoría mínima que admita el consumo |
| R33 | `categoría_actual = C` AND `energia > 6.700 kWh` | Subir a la categoría mínima que admita el consumo |
| R34 | `categoría_actual = D` AND `energia > 10.000 kWh` | Subir a la categoría mínima que admita el consumo |
| R35 | `categoría_actual = E` AND `energia > 13.000 kWh` | Subir a la categoría mínima que admita el consumo |
| R36 | `categoría_actual = F` AND `energia > 16.500 kWh` | Subir a la categoría mínima que admita el consumo |

> Las categorías G–K tienen el mismo límite máximo absoluto de 20.000 kWh. Si la energía supera ese valor, se genera la alerta R45.

---

## Bloque 3 (extensión) — Piso de categoría por empleados

Si el contribuyente declara empleados en relación de dependencia, la normativa establece una categoría mínima obligatoria. Este paso se aplica **después** del ajuste por parámetros físicos. CF = 1.0.

| N° | Condición | Consecuente |
|---|---|---|
| R48 | `empleados ≥ 1` AND `categoría_actual < B` | Recategorizar a **B** (piso mínimo) |
| R49 | `empleados ≥ 2` AND `categoría_actual < C` | Recategorizar a **C** (piso mínimo) |
| R50 | `empleados ≥ 3` AND `categoría_actual < D` | Recategorizar a **D** (piso mínimo) |

> Si la categoría ya supera el piso requerido, las reglas no producen ningún cambio.

---

## Bloque 4 — Alertas determinísticas de exclusión

Detecta condiciones que obligan o sugieren la salida del régimen. Las reglas con CF = 1.0 implican **exclusión obligatoria**; R37 (CF = 0.9) es una alerta de riesgo. Cuando R47 aplica, R37 es suprimida automáticamente.

| N° | Condición | Tipo de alerta | CF |
|---|---|---|---|
| R37 | `actividad = venta` AND `precio_unitario > $613.492,31` | Riesgo de exclusión por precio unitario | 0.9 |
| R38 | `alquiler > $2.390.229,80` AND `categoría ∈ {A, B}` | Exclusión por alquiler devengado | 1.0 |
| R39 | `alquiler > $3.266.647,39` AND `categoría ∈ {C, D}` | Exclusión por alquiler devengado | 1.0 |
| R40 | `alquiler > $4.143.064,98` AND `categoría ∈ {E, F}` | Exclusión por alquiler devengado | 1.0 |
| R41 | `alquiler > $4.939.808,23` AND `categoría = G` | Exclusión por alquiler devengado | 1.0 |
| R42 | `alquiler > $7.170.689,39` AND `categoría ∈ {H, I, J, K}` | Exclusión por alquiler devengado | 1.0 |
| R43 | `ingresos > $108.357.084,05` | Exclusión del régimen general | 1.0 |
| R44 | `superficie > 200 m²` | Exclusión por superficie | 1.0 |
| R45 | `energia > 20.000 kWh` | Exclusión por energía eléctrica | 1.0 |
| R46 | `alquiler > $7.170.689,39` (catch-all si R38–R42 no dispararon) | Exclusión por alquiler devengado | 1.0 |
| R47 | `actividad = venta` AND `precio_unitario > $613.492,31` | Exclusión obligatoria por precio unitario (supersede R37) | 1.0 |

> **Reglas de exclusión dura:** R38, R39, R40, R41, R42, R44, R45, R46, R47. Cuando alguna de estas se activa, `categoría_final = EXCLUIDO` e `impuesto_mensual = N/A`.

---

## Bloque 5 — Reglas del módulo difuso

### Variables de entrada

Cada variable de entrada es un porcentaje (0 a 1) calculado como:

| Variable | Cálculo |
|---|---|
| `presión_ingresos` | `ingresos / ingreso_max` de la categoría final |
| `presión_física` | `max(superficie / superficie_max, energia / energia_max)` de la categoría final |
| `presión_alquiler` | `alquiler / alquiler_max` de la categoría final |

### Conjuntos difusos de entrada (funciones trapezoidales)

| Conjunto | Pertenencia plena | Transición | Nula |
|---|---|---|---|
| **Baja** | 0% – 60% | 60% → 75% | ≥ 75% |
| **Media** | 75% – 85% | 60% → 75% (sube) / 85% → 95% (baja) | ≤ 60% o ≥ 95% |
| **Alta** | 95% – 100% | 85% → 95% | ≤ 85% |

### Conjuntos difusos de salida (funciones triangulares)

| Conjunto | Base | Centro (pico) | Rango numérico |
|---|---|---|---|
| **Estable** | 0 – 25 | 12 | 0 – 25 |
| **Precaución** | 20 – 50 | 37 | 26 – 50 |
| **Riesgo** | 45 – 75 | 62 | 51 – 75 |
| **Crítico** | 70 – 100 | 87 | 76 – 100 |

### Reglas difusas (RD1–RD27)

Las 27 reglas cubren las 3³ = 27 combinaciones posibles de los tres conjuntos de entrada. `AND = mínimo`, `OR = máximo` (método Mamdani). La defuzzificación usa el **método del centroide** sobre el universo [0, 100].

> **I** = presión_ingresos · **F** = presión_física · **A** = presión_alquiler

#### Consecuente: ESTABLE

| N° | I | F | A |
|---|---|---|---|
| RD1 | Baja | Baja | Baja |

#### Consecuente: PRECAUCIÓN

| N° | I | F | A |
|---|---|---|---|
| RD2 | Media | Baja | Baja |
| RD3 | Baja | Media | Baja |
| RD4 | Baja | Baja | Media |
| RD13 | Baja | Baja | Alta |
| RD14 | Baja | Media | Media |
| RD15 | Baja | Alta | Baja |

#### Consecuente: RIESGO

| N° | I | F | A |
|---|---|---|---|
| RD5 | Alta | Baja | Baja |
| RD6 | Media | Media | Baja |
| RD7 | Media | Baja | Media |
| RD8 | Media | Media | Media |
| RD16 | Baja | Media | Alta |
| RD17 | Baja | Alta | Media |
| RD18 | Baja | Alta | Alta |
| RD19 | Media | Baja | Alta |
| RD20 | Media | Media | Alta |
| RD21 | Media | Alta | Baja |
| RD22 | Media | Alta | Media |
| RD23 | Alta | Baja | Media |

#### Consecuente: CRÍTICO

| N° | I | F | A |
|---|---|---|---|
| RD9 | Alta | Media | Baja |
| RD10 | Alta | Alta | Media |
| RD11 | Alta | Alta | Alta |
| RD12 | Media | Alta | Alta |
| RD24 | Alta | Baja | Alta |
| RD25 | Alta | Media | Media |
| RD26 | Alta | Media | Alta |
| RD27 | Alta | Alta | Baja |

---

## Resumen de reglas por bloque

| Bloque | Reglas | Cantidad | Tipo |
|---|---|---|---|
| 1 — Ingresos servicios | R1–R12 | 12 | Determinística |
| 2 — Ingresos venta | R13–R24 | 12 | Determinística |
| 3 — Parámetros físicos | R25–R36 | 12 | Determinística |
| 3 ext — Empleados | R48–R50 | 3 | Determinística |
| 4 — Alertas de exclusión | R37–R47 | 11 | Determinística |
| 5 — Módulo difuso | RD1–RD27 | 27 | Difusa |
| **Total** | | **77** | |
