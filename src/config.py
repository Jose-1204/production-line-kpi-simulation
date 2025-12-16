
"""
Config de la simulacion de una linea de produccion.

Aqui se guardan los parametros del modelo en un solo lugar.
Para mayor facilidad de mantenimiento.
"""

# -----------------------------
# Parametros generales
# -----------------------------

DIAS_SIMULACION = 30
TURNOS = ["mañana", "tarde", "noche"]

DURACION_TURNO_HORAS = 8


# -----------------------------
# Produccion por turno
# -----------------------------
# Valores promedio y variabilidad por turno (unidades por turno)

PRODUCCION_POR_TURNO = {
    "mañana": {
        "media": 1050,
        "std": 40
    },
    "tarde": {
        "media": 1000,
        "std": 50
    },
    "noche": {
        "media": 950,
        "std": 60
    }
}


# -----------------------------
# Calidad por turno
# -----------------------------
# Tasa promedio de defectos por turno

TASA_DEFECTOS_POR_TURNO = {
    "mañana": 0.04,
    "tarde": 0.05,
    "noche": 0.06
}


# -----------------------------
# Paros operativos por turno
# -----------------------------
# Probabilidad de paro y duracion del paro en minutos

PAROS_POR_TURNO = {
    "mañana": {
        "probabilidad": 0.15,
        "tiempo_medio_min": 25,
        "tiempo_std_min": 8
    },
    "tarde": {
        "probabilidad": 0.20,
        "tiempo_medio_min": 30,
        "tiempo_std_min": 10
    },
    "noche": {
        "probabilidad": 0.25,
        "tiempo_medio_min": 35,
        "tiempo_std_min": 12
    }
}
