tengo que hacer un dashoboard dinamico con lo siguiente:
# Segmentación

## Primera pestaña

- El usuario debe poder cargar un archivo CSV que contenga variables numéricas y continuas.
- El usuario debe poder seleccionar las variables que desea considerar para el análisis.

## Segunda pestaña

- El usuario debe poder definir un rango de valores para el número de clusters.
- Con base en ese rango, se deben correr las soluciones de clustering utilizando LDA (Latent Dirichlet Allocation).
- Incluir una gráfica del codo y los indicadores AIC y BIC para ayudar a identificar el número óptimo de clusters.

## Tercera pestaña

- Mostrar, en una gráfica, las probabilidades de pertenencia de cada variable a cada solución.
- Esto permitirá visualizar qué variables son más relevantes para distinguir entre clusters.

## Cuarta pestaña

- Permitir al usuario agregar variables demográficas o cargar un nuevo archivo para hacer el merge con esas variables.
- Generar visualizaciones que crucen los clusters con las variables demográficas, para identificar proporciones y patrones.

## Exportables

- Generar un archivo Excel con:
- Tablas cruzadas de variables por cluster
- Una tabla con el RespondentID y su cluster asignado


## Dataset de pruebas

### Content
- AcceptedCmp1 - 1 if customer accepted the offer in the 1st campaign, 0 otherwise
- AcceptedCmp2 - 1 if customer accepted the offer in the 2nd campaign, 0 otherwise
- AcceptedCmp3 - 1 if customer accepted the offer in the 3rd campaign, 0 otherwise
- AcceptedCmp4 - 1 if customer accepted the offer in the 4th campaign, 0 otherwise
- AcceptedCmp5 - 1 if customer accepted the offer in the 5th campaign, 0 otherwise
- Response (target) - 1 if customer accepted the offer in the last campaign, 0 otherwise
- Complain - 1 if customer complained in the last 2 years
- DtCustomer - date of customer’s enrolment with the company
- Education - customer’s level of education
- Marital - customer’s marital status
- Kidhome - number of small children in customer’s household
- Teenhome - number of teenagers in customer’s household
- Income - customer’s yearly household income
- MntFishProducts - amount spent on fish products in the last 2 years
- MntMeatProducts - amount spent on meat products in the last 2 years
- MntFruits - amount spent on fruits products in the last 2 years
- MntSweetProducts - amount spent on sweet products in the last 2 years
- MntWines - amount spent on wine products in the last 2 years
- MntGoldProds - amount spent on gold products in the last 2 years
- NumDealsPurchases - number of purchases made with discount
- NumCatalogPurchases - number of purchases made using catalogue
- NumStorePurchases - number of purchases made directly in stores
- NumWebPurchases - number of purchases made through company’s web site
- NumWebVisitsMonth - number of visits to company’s web site in the last month
- Recency - number of days since the last purchase


Pasos a seguir:


* Tiene muchas **variables numéricas y continuas** (`Income`, `MntWines`, `NumWebPurchases`, etc.).
* Tiene **variables demográficas** (`Education`, `Marital`, `Kidhome`, etc.) que puedes usar en la cuarta pestaña.
* Puedes usar el campo `DtCustomer` como `RespondentID` si no hay uno explícito.

---

### Sobre el uso de **LDA (Latent Dirichlet Allocation)**


Para clustering de variables numéricas **lo adecuado es**:

* `K-Means` (más tradicional)
* `Gaussian Mixture Models (GMM)` (probabilístico)
* `DBSCAN` si hay ruido
* **BIC/AIC** se usan con **GMM**, no con LDA.

 **Entonces, lo más coherente sería usar GMM y no LDA**. Si tu profe se refirió a LDA por error, conviene que lo valides.



---

### Estructura  (por pestañas)

#### **1. Carga de datos**

* Subir CSV.
* Seleccionar variables numéricas para segmentación.

#### **2. Clustering (con GMM)**

* Rango de clusters (ej. 2 a 10).
* Mostrar:

  * Gráfica del codo (con BIC y AIC).
  * Elegir número óptimo visualmente.
* Guardar el cluster asignado por GMM.

#### **3. Visualización de importancia**

* Visualizar probabilidades de pertenencia (matriz de pertenencia de GMM).
* Mostrar heatmap o barplots de qué tan fuerte cada variable diferencia a cada cluster.

#### **4. Enriquecimiento con variables demográficas**

* Cargar segundo CSV o usar columnas como `Marital`, `Education`, `Kidhome`.
* Mostrar gráficos cruzados: por ejemplo, % de cluster por tipo de educación o estado civil.

#### **5. Exportables**

* Exportar Excel con:

  * `RespondentID`, cluster asignado.
  * Tablas cruzadas: cluster vs. variables demográficas.

---

### Estructura de carpetas

```plaintext
segmentacion_dashboard/
│
├── app.py                       # Archivo principal que levanta Streamlit
├── config.py                   # Configuración general (colores, título, etc.)
├── data/
│   ├── __init__.py
│   ├── loader.py               # Funciones para cargar y validar archivos CSV
│
├── pages/
│   ├── 1_carga_datos.py        # Página para cargar datos y seleccionar variables
│   ├── 2_clustering.py         # Clustering (GMM), gráfica del codo (AIC/BIC)
│   ├── 3_visualizacion.py      # Visualización de pertenencias y heatmaps
│   ├── 4_demograficos.py       # Merge con datos demográficos y gráficos
│
├── utils/
│   ├── __init__.py
│   ├── clustering.py           # Funciones para GMM, AIC/BIC, etc.
│   ├── plots.py                # Funciones de visualización (gráficas)
│   ├── export.py               # Funciones para generar archivos Excel
│
├── assets/                     # Imágenes, íconos o logos (si los quieres)
│
└── requirements.txt            # Dependencias del proyecto
```


