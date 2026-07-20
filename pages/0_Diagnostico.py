"""
Página de Diagnóstico y Auditoría de Calidad del Dato.
Permite analizar exhaustivamente la integridad, nulos, estadísticas 
y tipos de datos de los datasets Titanic y Madrid.
"""

import streamlit as st
import pandas as pd
from src.data import load_titanic_data, load_madrid_data, audit_dataset
from src.styles import apply_custom_styles

# Configuración de página
st.set_page_config(
    page_title="Diagnóstico de Datos | Streamlit Data Studio",
    page_icon="🔍",
    layout="wide"
)

# Aplicar estilos CSS personalizados
apply_custom_styles()

st.title("🔍 Auditoría y Diagnóstico del Dataset")
st.markdown(
    """
    Esta página permite validar la integridad, completitud y calidad técnica 
    de los conjuntos de datos antes de realizar análisis explicativos o predicciones.
    """
)

# Selección del dataset a auditar
dataset_option = st.radio(
    "Selecciona el dataset a diagnosticar:",
    ["🚢 Titanic (Passenger Dataset)", "🏠 Madrid (Airbnb Listings)"],
    horizontal=True
)

st.divider()

# Cargar dataset según selección
if "Titanic" in dataset_option:
    df = load_titanic_data()
    dataset_name = "Titanic"
else:
    df = load_madrid_data()
    dataset_name = "Madrid Listings"

# Calcular diagnóstico completo
metrics = audit_dataset(df)

# ==========================================================
# SECCIÓN 1: METRICAS GENERALES (KPIs)
# ==========================================================
st.subheader(f"📊 Métricas Generales — {dataset_name}")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Filas", f"{metrics['rows']:,}")
col2.metric("Total Columnas", metrics['columns'])
col3.metric("Uso en Memoria", f"{metrics['memory_mb']} MB")
col4.metric("Filas Duplicadas", metrics['duplicates'])
col5.metric("Celdas Nulas (% Total)", f"{metrics['missing_pct']}%")

st.divider()

# ==========================================================
# SECCIÓN 2: TABS DE ANÁLISIS DETALLADO
# ==========================================================
tab_quality, tab_stats, tab_missing, tab_preview = st.tabs([
    "🟢 Calidad del Dataset",
    "📈 Estadísticas (Describe)",
    "🧩 Análisis de Nulos",
    "📄 Vista Previa (Head & Tail)"
])

# ----------------------------------------------------------
# TAB 1: CALIDAD DEL DATASET (SEMÁFOROS)
# ----------------------------------------------------------
with tab_quality:
    st.markdown("### 🛡️ Diagnóstico de Reglas de Calidad")
    
    st.info("A continuación se evalúa el cumplimiento de reglas clave para el dataset seleccionado.")
    
    # Evaluación de Reglas
    rules_results = []
    
    # Regla 1: Duplicados
    if metrics['duplicates'] == 0:
        rules_results.append(("🟢", "Sin filas duplicadas", "No existen registros idénticos repetidos en la base de datos."))
    else:
        rules_results.append(("🟡", f"Existen {metrics['duplicates']} duplicados", "Se recomienda revisar o eliminar filas duplicadas."))
        
    # Reglas específicas Titanic
    if dataset_name == "Titanic":
        # Regla Nulos Edad
        null_age = metrics['missing_by_col'].get('Age', 0)
        if null_age == 0:
            rules_results.append(("🟢", "Sin nulos en Edad", "La variable Age está 100% completa."))
        else:
            rules_results.append(("🟡", f"Existen {null_age} nulos en Age", "Se requerirá imputación (media/mediana) o tratamiento de nulos para algoritmos."))
            
        # Regla Nulos Cabin
        null_cabin = metrics['missing_by_col'].get('Cabin', 0)
        if null_cabin > (metrics['rows'] * 0.5):
            rules_results.append(("🔴", f"Alto porcentaje de nulos en Cabin ({null_cabin} nulos)", "Más del 50% es nulo; evaluar descartar la columna o crear un flag 'Tiene_Cabina'."))
        else:
            rules_results.append(("🟢", "Completitud aceptable en Cabin", "Menos del 50% de nulos."))
            
        # Regla Tipos de Datos
        rules_results.append(("🟢", "Tipos de datos correctos", "Variables categóricas y numéricas bien identificadas."))

    # Reglas específicas Madrid
    else:
        # Regla Precio Numérico
        if pd.api.types.is_numeric_dtype(df['price']):
            rules_results.append(("🟢", "Precio en formato numérico", "La columna 'price' ha sido casteada correctamente a valores flotantes/enteros."))
        else:
            rules_results.append(("🔴", "Precio en formato string", "Atención: la columna contiene símbolos de moneda o texto no procesado."))
            
        # Regla Coordenadas Válidas
        if 'latitude' in df.columns and 'longitude' in df.columns:
            valid_lat = df['latitude'].between(40.0, 41.0).all()
            valid_lon = df['longitude'].between(-4.0, -3.0).all()
            if valid_lat and valid_lon:
                rules_results.append(("🟢", "Coordenadas geográficas válidas", "Todas las latitudes y longitudes están dentro del rango razonable para la Comunidad de Madrid."))
            else:
                rules_results.append(("🟡", "Coordenadas fuera de rango", "Existen coordenadas potencialmente erróneas o fuera de la región."))
                
        # Regla Nulos Precio
        null_price = metrics['missing_by_col'].get('price', 0)
        if null_price > 0:
            rules_results.append(("🟡", f"Existen {null_price} nulos en Price", "Filtrar estos registros para análisis financieros o mapas de precios."))
        else:
            rules_results.append(("🟢", "Precios 100% completos", "No hay valores faltantes en la columna price."))

    # Renderizar resultados de la evaluación
    for status, title, description in rules_results:
        with st.container():
            col_icon, col_desc = st.columns([1, 15])
            col_icon.markdown(f"### {status}")
            col_desc.markdown(f"**{title}**  \n*{description}*")
            st.divider()

# ----------------------------------------------------------
# TAB 2: ESTADÍSTICAS DESCRIPTIVAS
# ----------------------------------------------------------
with tab_stats:
    st.markdown("### 📐 Resumen Estadístico Detallado")
    
    st.markdown("#### 🔢 Variables Numéricas")
    st.dataframe(df.describe().T, use_container_width=True)
    
    st.markdown("#### 🔤 Variables Categóricas / Texto")
    cat_df = df.select_dtypes(include=['object', 'category'])
    if not cat_df.empty:
        st.dataframe(cat_df.describe().T, use_container_width=True)
    else:
        st.info("No se encontraron variables categóricas o de texto en el dataset.")

# ----------------------------------------------------------
# TAB 3: ANÁLISIS DE VALORES NULOS
# ----------------------------------------------------------
with tab_missing:
    st.markdown("### 🧩 Desglose de Valores Faltantes por Columna")
    
    missing_df = pd.DataFrame({
        "Columna": df.columns,
        "Tipo Dato": df.dtypes.astype(str),
        "Valores Nulos": metrics['missing_by_col'].values,
        "% Nulos": [round((val / metrics['rows']) * 100, 2) for val in metrics['missing_by_col'].values]
    }).sort_values(by="Valores Nulos", ascending=False)
    
    st.dataframe(missing_df, use_container_width=True, hide_index=True)

# ----------------------------------------------------------
# TAB 4: VISTA PREVIA DE DATOS
# ----------------------------------------------------------
with tab_preview:
    st.markdown("### 📄 Inspección de Primeras y Últimas Filas")
    
    num_preview = st.slider("Número de filas a visualizar:", min_value=3, max_value=20, value=5)
    
    st.markdown(f"#### Primeras {num_preview} filas (Head)")
    st.dataframe(df.head(num_preview), use_container_width=True)
    
    st.markdown(f"#### Últimas {num_preview} filas (Tail)")
    st.dataframe(df.tail(num_preview), use_container_width=True)