import numpy as np
import pandas as pd
from pathlib import Path


# Se importan los parámetros definidos en config.py
from config import (
    DIAS_SIMULACION,
    TURNOS,
    DURACION_TURNO_HORAS,
    PRODUCCION_POR_TURNO,
    TASA_DEFECTOS_POR_TURNO,
    PAROS_POR_TURNO,
)

def safe_int(value):
    """
    Convierte a entero y elimina valores negativos.
    Lo usamos porque la producción y los paros no pueden ser negativos.
    """
    return int(max(0, round(value)))

def simulate_shift(day, shift, rng):
    """
    Simula un solo turno de producción para un día específico.
    Devuelve un diccionario con los datos del turno.
    """

    # 1. Producción base (antes de considerar paros)
    prod_config = PRODUCCION_POR_TURNO[shift]
    base_production = rng.normal(
        loc=prod_config["media"],
        scale=prod_config["std"]
    )
    base_production = safe_int(base_production)

    # 2. Ver si ocurre un paro en el turno
    paro_config = PAROS_POR_TURNO[shift]
    ocurre_paro = rng.random() < paro_config["probabilidad"]

    downtime_minutes = 0
    if ocurre_paro:
        downtime = rng.normal(
            loc=paro_config["tiempo_medio_min"],
            scale=paro_config["tiempo_std_min"]
        )
        downtime_minutes = safe_int(downtime)

    # 3. Ajustar producción según el tiempo de paro
    minutos_turno = DURACION_TURNO_HORAS * 60

    # El paro no puede ser mayor que la duración total del turno
    downtime_minutes = min(downtime_minutes, minutos_turno)

    # Proporción de tiempo realmente trabajado
    disponibilidad = 1 - (downtime_minutes / minutos_turno)

    # Producción final del turno
    unidades_producidas = safe_int(base_production * disponibilidad)

    # 4. Cálculo de unidades defectuosas
    tasa_defectos = TASA_DEFECTOS_POR_TURNO[shift]
    unidades_defectuosas = rng.binomial(
        n=unidades_producidas,
        p=tasa_defectos
    )

    return {
        "day": day,
        "shift": shift,
        "units_produced": unidades_producidas,
        "units_defective": int(unidades_defectuosas),
        "downtime_minutes": int(downtime_minutes),
    }

def generate_dataset(seed=42):
    """
    Genera el dataset completo recorriendo días y turnos.
    """
    rng = np.random.default_rng(seed)
    data = []

    for day in range(1, DIAS_SIMULACION + 1):
        for shift in TURNOS:
            row = simulate_shift(day, shift, rng)
            data.append(row)

    df = pd.DataFrame(data)

    # Validaciones para asegurar coherencia
    assert (df["units_produced"] >= 0).all()
    assert (df["units_defective"] >= 0).all()
    assert (df["downtime_minutes"] >= 0).all()
    assert (df["units_defective"] <= df["units_produced"]).all()

    return df

def main():
    # Se obtiene la ruta raíz del proyecto
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data"
    data_path.mkdir(exist_ok=True)

    output_file = data_path / "production_data.csv"

    # Generar datos
    df = generate_dataset(seed=42)
    df.to_csv(output_file, index=False)

    # Resumen rápido para verificar que todo tenga sentido
    total_production = int(df["units_produced"].sum())
    total_defects = int(df["units_defective"].sum())
    total_downtime = int(df["downtime_minutes"].sum())

    defect_rate = (
        total_defects / total_production
        if total_production > 0 else 0
    )

    print("DATASET GENERADO")
    print("=" * 40)
    print(f"Filas generadas: {len(df)}")
    print(f"Archivo creado: {output_file}")
    print("-" * 40)
    print(f"Unidades producidas: {total_production}")
    print(f"Unidades defectuosas: {total_defects}")
    print(f"Tasa de defectos global: {defect_rate:.2%}")
    print(f"Tiempo total de paro (min): {total_downtime}")

if __name__ == "__main__":
    main()
