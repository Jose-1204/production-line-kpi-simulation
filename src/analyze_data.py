import pandas as pd
from pathlib import Path


def load_data():
    """
    Carga el archivo CSV generado por el script de simulación.
    """
    project_root = Path(__file__).resolve().parents[1]
    data_file = project_root / "data" / "production_data.csv"

    df = pd.read_csv(data_file)
    return df


def analyze_by_shift(df):
    """
    Analiza el desempeño agrupando los datos por turno.
    """
    summary = df.groupby("shift").agg(
        total_units_produced=("units_produced", "sum"),
        avg_units_produced=("units_produced", "mean"),
        total_defective=("units_defective", "sum"),
        avg_downtime=("downtime_minutes", "mean")
    )

    #Calcula cuántos defectos hubo por turno
    summary["defect_rate"] = (
        summary["total_defective"] / summary["total_units_produced"]
    )

    return summary


def print_report(summary):
    """
    Imprime un reporte claro en consola con una conclusión final.
    """
    print("RESUMEN DE DESEMPEÑO POR TURNO")
    print("=" * 40)

    worst_shift = None
    worst_score = -1

    for shift in summary.index:
        row = summary.loc[shift]

        print(f"\nTurno: {shift}")
        print(f"Producción total: {int(row['total_units_produced'])}")
        print(f"Producción promedio: {row['avg_units_produced']:.2f}")
        print(f"Tasa de defectos: {row['defect_rate']:.2%}")
        print(f"Downtime promedio (min): {row['avg_downtime']:.2f}")

        #identificar el peor turno
        score = row["defect_rate"] + (row["avg_downtime"] / 100)

        if score > worst_score:
            worst_score = score
            worst_shift = shift

    print("\nCONCLUSIÓN")
    print("-" * 40)
    print(
        f"El turno con peor desempeño general es el turno '{worst_shift}', "
        "presenta una combinación más alta de defectos y tiempo de paro."
    )

    """
    Imprime un reporte  claro en consola con una conclusión final.
    """
    print("RESUMEN DE DESEMPEÑO POR TURNO")
    print("=" * 40)

    worst_shift = None
    worst_score = -1

    for shift, row in summary.iterrows():
        print(f"\nTurno: {shift}")
        print(f"Producción total: {int(row['total_units_produced'])}")
        print(f"Producción promedio: {row['avg_units_produced']:.2f}")
        print(f"Tasa de defectos: {row['defect_rate']:.2%}")
        print(f"Downtime promedio (min): {row['avg_downtime']:.2f}")

        # Metrica para identificar peor turno
        score = row["defect_rate"] + (row["avg_downtime"] / 100)

        if score > worst_score:
            worst_score = score
            worst_shift = shift

    print("\nCONCLUSIÓN")
    print("-" * 40)
    print(
        f"El turno con peor desempeño general es el turno '{worst_shift}', "
        "presenta una combinación más alta de  defectos y tiempo de paro."
    )


def main():
    df = load_data()
    summary = analyze_by_shift(df)
    print_report(summary)


if __name__ == "__main__":
    main()
