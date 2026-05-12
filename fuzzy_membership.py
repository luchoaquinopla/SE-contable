

def membresia_trapezoidal(x, a, b, c, d):
    """
    Grado de pertenencia de x a un trapecio [a, b, c, d].

        0 si x <= a o x >= d
        sube de 0 a 1 entre a y b  (rampa ascendente)
        1 si b <= x <= c           (zona de pertenencia plena)
        baja de 1 a 0 entre c y d  (rampa descendente)
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
    Grado de pertenencia de x a un triángulo [a, b, c].

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



# Conjuntos difusos de ENTRADA — presión (valor entre 0 y 1)
# Cada función devuelve el grado de pertenencia al conjunto baja/media/alta.


def presion_baja(p):
    """Pertenencia plena si p <= 0.60, transición entre 0.60 y 0.75, nula si p >= 0.75"""
    return membresia_trapezoidal(p, -0.01, 0.0, 0.60, 0.75)

def presion_media(p):
    """Transición ascendente entre 0.60 y 0.75, plena entre 0.75 y 0.85, descendente hasta 0.95"""
    return membresia_trapezoidal(p, 0.60, 0.75, 0.85, 0.95)

def presion_alta(p):
    """Transición ascendente entre 0.85 y 0.95, pertenencia plena desde 0.95"""
    return membresia_trapezoidal(p, 0.85, 0.95, 1.0, 1.01)



# Conjuntos difusos de SALIDA — riesgo fiscal (valor entre 0 y 100)


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
