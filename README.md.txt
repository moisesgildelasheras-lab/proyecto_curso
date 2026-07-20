# 🚀 Streamlit Data Studio

Plataforma modular e interactiva para el Análisis Exploratorio de Datos (EDA) y la Auditoría de Calidad sobre los conjuntos de datos de **Titanic** y **Madrid Airbnb Listings**.

---

## 📂 Arquitectura del Proyecto

El proyecto sigue el principio de separación de responsabilidades (*Separation of Concerns*), desacoplando la lógica de negocio, la preparación de datos y los componentes de UI:

```text
proyecto_final/
│
├── app.py                      # Punto de entrada (Landing Page)
│
├── pages/                      # Vistas y paneles interactivos
│   ├── 0_Diagnostico.py        # Auditoría de datos y reglas de calidad
│   ├── 1_Titanic.py            # Dashboard analítico del Titanic
│   ├── 2_Madrid.py             # Dashboard financiero y mapa interactivo
│   └── 3_Galeria.py            # Laboratorio de correlaciones y gráficos
│
├── src/                        # Módulos de lógica centralizada
│   ├── __init__.py
│   ├── data.py                 # Carga, limpieza y auditoría
│   ├── filters.py              # Gestión centralizada de filtros
│   ├── metrics.py              # Cálculo puro de KPIs
│   ├── charts.py               # Fábrica de gráficos Plotly
│   ├── maps.py                 # Visualización geográfica
│   ├── utils.py                # Formateadores y utilidades
│   └── styles.py               # Inyección de estilos CSS
│
├── data/                       # Datasets fuente (.csv)
├── tests/                      # Pruebas unitarias automatizadas
├── requirements.txt            # Dependencias del proyecto
└── README.md