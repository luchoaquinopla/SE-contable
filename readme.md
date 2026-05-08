# Sistema Experto de Categorización de Monotributo

**Asignatura:** Sistemas Inteligentes — Práctica de Laboratorio N° 9  
**Carrera:** Ingeniería en Sistemas de Información  
**Normativa base:** ARCA (ex AFIP) — Vigente desde 01/02/2026

---

## ¿Qué hace este sistema?

Este programa es un **Sistema Experto híbrido** que asesora a contribuyentes inscriptos (o que quieren inscribirse) en el **Régimen Simplificado para Pequeños Contribuyentes (Monotributo)** de Argentina.

Dado un conjunto de datos del contribuyente, el sistema determina:

1. **Qué categoría de Monotributo le corresponde** (de la A a la K), según sus ingresos, tipo de actividad y parámetros físicos.
2. **Si existen alertas de exclusión del régimen** (alquiler excedido, precio unitario excedido, ingresos fuera del régimen).
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
├── main.py              # Punto de entrada. Menú principal y modos de uso.
├── knowledge_base.py    # Base de conocimiento: datos normativos y funciones de membresía.
├── inference_engine.py  # Motor de inferencia determinístico (Bloques 1 a 4).
├── fuzzy_engine.py      # Motor de lógica difusa (Bloque 5).
├── expert_system.py     # Módulo integrador: orquesta los tres módulos y muestra resultados.
├── test_cases.py        # Los 7 casos de prueba predefinidos.
└── README.md            # Este archivo.
```

---

## Descripción de cada archivo

### `knowledge_base.py` — Base de Conocimiento

Contiene **todo el conocimiento normativo** del sistema. Es el único archivo que habría que actualizar si cambian los valores de ARCA. Incluye:

- `CATEGORIAS`: diccionario con los límites de ingreso, superficie, energía y alquiler de cada categoría (A a K), más el impuesto integrado mensual según tipo de actividad.
- `ORDEN_CATEGORIAS`: lista ordenada de categorías usada para la lógica de recategorización.
- `PRECIO_UNITARIO_MAX` e `INGRESO_MAX_REGIMEN`: constantes del régimen.
- Funciones de membresía difusa: `presion_baja()`, `presion_media()`, `presion_alta()` para las entradas, y `riesgo_estable()`, `riesgo_precaucion()`, `riesgo_zona_riesgo()`, `riesgo_critico()` para la salida.

### `inference_engine.py` — Motor de Inferencia Determinístico

Implementa el **encadenamiento hacia adelante** para los cuatro bloques de reglas determinísticas:

| Función                               | Bloque | Reglas  | Qué hace                                                              |
| ------------------------------------- | ------ | ------- | --------------------------------------------------------------------- |
| `determinar_categoria_por_ingresos()` | 1 y 2  | R1–R24  | Asigna categoría base según ingresos y actividad                      |
| `ajustar_por_parametros_fisicos()`    | 3      | R25–R36 | Sube la categoría si superficie o energía lo requieren                |
| `detectar_alertas()`                  | 4      | R37–R43 | Detecta alertas de exclusión por alquiler, precio unitario o ingresos |

Cada función devuelve un diccionario con el resultado y las reglas activadas, que alimentan el subsistema de explicación.

### `fuzzy_engine.py` — Motor de Lógica Difusa

Implementa el **Bloque 5** en tres pasos:

| Función                    | Paso                | Qué hace                                                             |
| -------------------------- | ------------------- | -------------------------------------------------------------------- |
| `calcular_presiones()`     | Previo              | Calcula los tres porcentajes de presión (ingresos, física, alquiler) |
| `fuzzificar()`             | 1 — Fuzzificación   | Convierte las presiones en grados de pertenencia (baja/media/alta)   |
| `aplicar_reglas_difusas()` | 2 — Inferencia      | Aplica las 12 reglas difusas (RD1–RD12) con AND=mínimo, OR=máximo    |
| `defuzzificar()`           | 3 — Defuzzificación | Aplica el método del centroide para obtener el valor numérico 0–100  |
| `interpretar_riesgo()`     | Post                | Convierte el valor numérico en etiqueta lingüística                  |
| `evaluar_riesgo_difuso()`  | Orquestador         | Llama a todas las anteriores en orden                                |

### `expert_system.py` — Módulo Integrador

Es el cerebro del sistema. La función principal `ejecutar_sistema_experto(caso)` orquesta los tres módulos en orden y devuelve el diagnóstico completo. La función `mostrar_resultado(resultado)` implementa el **subsistema de explicación**, mostrando en consola de forma clara y estructurada la categoría, las alertas, el nivel de riesgo y las reglas que se activaron.

### `test_cases.py` — Casos de Prueba

Contiene los 7 casos de prueba predefinidos. Cada caso es un diccionario con las entradas del contribuyente. Los casos cubren:

| Caso      | Escenario                           | Qué valida                          |
| --------- | ----------------------------------- | ----------------------------------- |
| Caso 1    | Diseñador gráfico, categoría A      | Caso simple, situación estable      |
| Caso 2    | Contador con oficina grande         | Recategorización por superficie     |
| Caso 3    | Comerciante de ropa, ingresos altos | Zona crítica por presión combinada  |
| Caso 4    | Odontóloga con alquiler caro        | Alerta de exclusión por alquiler    |
| Caso 5    | Vendedor de electrónica             | Alerta por precio unitario excedido |
| Caso 6    | Médico de altos ingresos            | Exclusión total del régimen         |
| Caso 7 ⚠️ | Electricista al 91% del límite      | **Caso límite/ambiguo**             |

### `main.py` — Punto de Entrada

Gestiona los dos modos de uso del sistema: interactivo (el usuario ingresa datos por consola) y automático (ejecuta los casos de prueba predefinidos). No contiene lógica del SE.

---

## Flujo del sistema

```
Datos del contribuyente
        │
        ▼
[inference_engine] Bloque 1/2: ¿Qué categoría por ingresos?
        │
        ▼
[inference_engine] Bloque 3: ¿Hay que recategorizar por parámetros físicos?
        │
        ▼
[inference_engine] Bloque 4: ¿Hay alertas de exclusión?
        │
        ▼
[fuzzy_engine] Bloque 5: ¿Cuál es el riesgo fiscal global?
   → Calcular presiones → Fuzzificar → Inferir → Defuzzificar
        │
        ▼
[expert_system] Subsistema de explicación: mostrar resultado completo
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
  Reglas: R2, RD5, RD6, RD7, RD8...

  1. [R2] Ingresos $13,703,187 dentro del límite de Cat. B ($15,058,447). CF=1.0
  2. Superficie y energía coherentes con categoría B.
```

---

## Notas importantes

- Los valores normativos están **actualizados a la tabla vigente desde 01/02/2026** publicada por ARCA.
- El parámetro de superficie **no aplica en localidades de menos de 40.000 habitantes**, según la normativa. El sistema asume que el contribuyente está en una localidad donde aplica.
- El sistema es una herramienta de orientación. Para decisiones impositivas definitivas, consultar siempre a un contador público matriculado.
