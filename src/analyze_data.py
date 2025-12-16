import pandas as pd
from pathlib import Path


def load_data():
    """
    Carga el CSV
    """
    project_root = Path(__file__).resolve().parents[1]
    data_file = project_root / "data" / "production_data.csv"

    df = pd.read_csv(data_file)
    return df


def analyze_by_shift(df):
    """
    Analiza agrupando los datos por turno.
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
    Reporte en consola.
    """
    print("RESUMEN DE DESEMPEÑO POR TURNO")
    print("=" * 40)

    for shift, row in summary.iterrows():
        print(f"\nTurno: {shift}")
        print(f"Producción total: {int(row['total_units_produced'])}")
        print(f"Producción promedio: {row['avg_units_produced']:.2f}")
        print(f"Tasa de defectos: {row['defect_rate']:.2%}")
        print(f"Downtime promedio (min): {row['avg_downtime']:.2f}")

    # encontrar el peor turno en calidad y en downtime
    worst_quality_shift = summary["defect_rate"].idxmax()
    worst_downtime_shift = summary["avg_downtime"].idxmax()

    print("\nCONCLUSIÓN")
    print("-" * 40)
    print(f"Peor turno en calidad (mayor tasa de defectos): '{worst_quality_shift}'.")
    print(f"Peor turno en paros (mayor downtime promedio): '{worst_downtime_shift}'.")
    print(
        "Para reducir defectos (calidad), "
        f"el turno problematico es '{worst_quality_shift}'."
    )

def main():
    df = load_data()
    summary = analyze_by_shift(df)
    print_report(summary)


if __name__ == "__main__":
    main()
