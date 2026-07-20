"""
Página Dashboard — Análisis Exploratorio del Titanic.
"""

import streamlit as st
from src.data import load_titanic_data
from src.filters import render_titanic_filters
from src.metrics import get_titanic_kpis
from src.charts import (
    plot_survival_by_class,
    plot_age_distribution_by_survival,
    plot_fare_vs_age_scatter,
    plot_embarked_pie
)
from src.styles import apply_custom_styles

# Configuración de la página
st.set_page_config(
    page_title="Titanic Dashboard | Streamlit Data Studio",
    page_icon="🚢",
    layout="wide"
)

# Estilos personalizados
apply_custom_styles()

# 1. Cargar datos base
df_raw = load_titanic_data()

# 2. Renderizar Filtros Laterales Centralizados
df_filtered = render_titanic_filters(df_raw)

# Encabezado
st.title("🚢 Dashboard Analítico — Titanic")
st.caption("Análisis interactivo de la demografía, tarifas y factores de supervivencia del pasaje.")

st.divider()

# Si los filtros dejan el dataset vacío, mostrar advertencia defensiva
if df_filtered.empty:
    st.warning("⚠️ No se encontraron registros con los filtros seleccionados en el panel lateral.")
    st.stop()

# 3. MÓDULO DE KPIs
kpis = get_titanic_kpis(df_filtered)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Pasajeros Seleccionados", f"{kpis['total_passengers']:,}")
c2.metric("Supervivientes", f"{kpis['survivors']:,}")
c3.metric("Tasa de Supervivencia", f"{kpis['survival_rate']}%")
c4.metric("Edad Media", f"{kpis['avg_age']} años")
c5.metric("Tarifa Media", f"{kpis['avg_fare']} £")

st.divider()

# 4. TABS DE VISUALIZACIÓN Y ANÁLISIS
tab_overview, tab_demographics, tab_correlations, tab_data = st.tabs([
    "📊 Resumen de Supervivencia",
    "👥 Demografía & Puertos",
    "📈 Tarifas & Correlaciones",
    "📋 Datos Filtrados"
])

# --- TAB 1: RESUMEN DE SUPERVIVENCIA ---
with tab_overview:
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig_class = plot_survival_by_class(df_filtered)
        st.plotly_chart(fig_class, use_container_width=True)
        
    with col_right:
        fig_age = plot_age_distribution_by_survival(df_filtered)
        st.plotly_chart(fig_age, use_container_width=True)

# --- TAB 2: DEMOGRAFÍA Y PUERTOS ---
with tab_demographics:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        fig_pie = plot_embarked_pie(df_filtered)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_right:
        st.markdown("#### 💡 Insights Demográficos")
        st.info(
            """
            * **Efecto 'Mujeres y niños primero':** Históricamente las tasas de supervivencia son significativamente superiores en el género femenino y en los rangos de edad infantiles.
            * **Impacto del Puerto de Embarque:** Cherbourg (C) registró en proporción una mayor concentración de pasajeros de 1ª Clase respecto a Southampton (S) o Queenstown (Q).
            """
        )

# --- TAB 3: TARIFAS Y CORRELACIONES ---
with tab_correlations:
    fig_scatter = plot_fare_vs_age_scatter(df_filtered)
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- TAB 4: DATOS FILTRADOS ---
with tab_data:
    st.markdown("### 📋 Vista de Registros Filtrados")
    st.caption("Esta tabla refleja exactamente la selección realizada desde los filtros laterales.")
    
    st.dataframe(
        df_filtered[['PassengerId', 'Name', 'Sex', 'Age', 'Pclass', 'Fare', 'Embarked', 'Survived']],
        use_container_width=True,
        hide_index=True
    )