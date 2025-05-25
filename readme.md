# Dashboard Dinámico de Segmentación de Clientes

Este proyecto implementa un dashboard interactivo en Streamlit para realizar segmentación de clientes utilizando técnicas de clustering (GMM/K-Means), visualización avanzada y análisis demográfico. El código está modularizado siguiendo buenas prácticas y principios SOLID.

---

## Estructura del Dashboard

### 1. Carga de Datos

- Permite cargar un archivo CSV con variables numéricas y continuas.
- El usuario puede seleccionar las variables que desea considerar para el análisis de segmentación.
- Validación de identificador único para cada registro.

### 2. Clustering

- El usuario define un rango para el número de clusters.
- Se ejecutan algoritmos de clustering (Gaussian Mixture Models y K-Means).
- Se muestran métricas como AIC, BIC (para GMM) y el método del codo (para K-Means).
- Se calcula el Silhouette Score para evaluar la calidad de los clusters.
- El usuario puede seleccionar el número óptimo de clusters y asignar los clusters al dataset.

### 3. Visualización de Pertenencias

- Visualización de la matriz de pertenencia (probabilidades de pertenencia a cada cluster) mediante heatmap.
- Visualización de reducción de dimensionalidad (PCA 2D y 3D) para explorar la separación de los clusters.
- Permite identificar qué variables son más relevantes para distinguir entre clusters.

### 4. Enriquecimiento Demográfico

- Permite cargar un segundo archivo CSV con variables demográficas o seleccionar columnas demográficas del dataset original.
- Realiza el merge entre los clusters y las variables demográficas.
- Genera visualizaciones cruzadas: heatmaps, boxplots, radar charts y gráficos de barras para analizar la composición demográfica de cada cluster.

### 5. Exportables

- Permite descargar un archivo Excel con:
  - Tablas cruzadas de variables demográficas por cluster.
  - Una tabla con el identificador único y el cluster asignado para cada registro.
  - Todos los datos combinados.

---

## Estructura de Carpetas

```
proyecto/
│
├── app.py                       # Archivo principal de Streamlit
├── config.py                    # Configuración global (título, layout, etc.)
├── data/
│   └── loader.py                # Carga y validación de archivos CSV
├── pages_app/
│   ├── cargar_datos.py          # Página 1: carga y selección de variables
│   ├── generar_cluster.py       # Página 2: clustering y métricas
│   ├── vizualizacion.py         # Página 3: visualización de pertenencias
│   └── add_demografico.py       # Página 4: merge y análisis demográfico
├── utils/
│   ├── cleaning.py              # Limpieza y normalización de datos
│   ├── clustering.py            # Algoritmos y métricas de clustering
│   ├── plots.py                 # Visualizaciones y gráficos
│   └── export.py                # Exportación de resultados a Excel
└── requirements.txt             # Dependencias del proyecto
```

---

## Dataset de Prueba

Incluye variables numéricas y demográficas como:

- `Income`, `MntWines`, `NumWebPurchases`, etc. (numéricas)
- `Education`, `Marital`, `Kidhome`, etc. (demográficas)
- Puedes usar `DtCustomer` como identificador si no hay uno explícito.

---

## Requisitos

- Python 3.8+
- Streamlit
- pandas, scikit-learn, plotly, xlsxwriter

Instala dependencias con:

```bash
pip install -r requirements.txt
```

---

## Ejecución

Desde la raíz del proyecto:

```bash
streamlit run app.py
```

---

## Notas Técnicas

- El dashboard está modularizado y orientado a buenas prácticas (SOLID).
- El clustering se realiza con GMM y K-Means.
- El código es fácilmente extensible y mantenible.
- El usuario puede exportar todos los resultados y análisis en un solo archivo Excel.

---

## Créditos

Desarrollado por Misael Ramos para la materia de Ciencia de Datos / Marketing.


