# Production Line KPI Simulation

Este proyecto simula una linea de produccion sencilla con el objetivo de analizar
el desempeno de los turnos de trabajo usando datos generados artificialmente

Este proyecto es una practica de analisis de datos 
aplicada a la ingenieria industrial

---

## Objetivo

Analizar que turno presenta peor desempeno considerando dos aspectos clave:
- tasa de defectos (calidad)
- tiempo de paro promedio (downtime)

El analisis permite identificar diferencias entre turnos y entender
donde pueden existir problemas operativos

---
## Estructura del proyecto

- `src/`
  - `config.py`: parametros de la simulacion (turnos, produccion, defectos, paros)
  - `generate_data.py`: genera datos simulados de produccion en formato CSV
  - `analyze_data.py`: analiza los datos y muestra un resumen por turno en consola
- `data/`
  - contiene los archivos CSV generados 
- `notebooks/`
  - carpeta para visualizaciones futuras

---
## Flujo del proyecto

1. Se definen parametros de simulacion por turno
2. Se generan datos diarios de produccion, defectos y paros
3. Se analizan los datos agrupando por turno
4. Se imprime un reporte con conclusiones claras

---

## ejecutar el proyecto

```bash
pip install -r requirements.txt
python src/generate_data.py 
python src/analyze_data.py
```

