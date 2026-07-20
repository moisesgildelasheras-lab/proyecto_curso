"""
Página Dashboard — Análisis de la Oferta Turística en Madrid.
"""

import streamlit as st
from src.data import load_madrid_data
from src.filters import render_madrid_filters
from src.metrics import get_madrid_kpis
from src.charts import plot_price_by_neighbourhood, plot_room_type_distribution
from src.maps import plot_madrid_map
from src.styles import apply_custom_styles

# Configuración de página
st.set_page_config(
    page_title="Madrid Airbnb Dashboard | Streamlit Data Studio",
    page_icon="🏠",
    layout="wide"
)

apply_custom_styles()

# 1. Cargar datos
df_raw = load_madrid_data()

# 2. Renderizar Filtros
df_filtered = render_madrid_filters(df_raw)

# Encabezado
st.title("🏠 Dashboard Analítico — Madrid Listings")
st.caption("Exploración espacial y financiera de la oferta turística en la Comunidad de Madrid.")

st.divider()

if df_filtered.empty:
    st.warning("⚠️ No se encontraron alojamientos con los filtros seleccionados.")
    st.stop()

# 3. KPIs
kpis = get_madrid_kpis(df_filtered)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Alojamientos", f"{kpis['total_listings']:,}")
c2.metric("Precio Medio", f"{kpis['avg_price']} €")
c3.metric("Precio Mediana", f"{kpis['median_price']} €")
c4.metric("Disponibilidad Media", f"{kpis['avg_availability']} días/año")
c5.metric("Total Reseñas", f"{kpis['total_reviews']:,}")

st.divider()

# 4. TABS
tab_map, tab_prices, tab_data = st.tabs([
    "🗺️ Mapa Interactivo",
    "📊 Precios & Tipologías",
    "📋 Datos Filtrados"
])

with tab_map:
    st.markdown("### 📍 Mapa de Distribución Geográfica")
    fig_map = plot_madrid_map(df_filtered)
    st.plotly_chart(fig_map, use_container_width=True)

with tab_prices:
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig_bar = plot_price_by_neighbourhood(df_filtered)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_right:
        fig_pie = plot_room_type_distribution(df_filtered)
        st.plotly_chart(fig_pie, use_container_width=True)

with tab_data:
    st.markdown("### 📋 Listado de Alojamientos Filtrados")
    st.dataframe(
        df_filtered[['id', 'name', 'neighbourhood_group', 'room_type', 'price', 'minimum_nights', 'number_of_reviews']],
        use_container_width=True,
        hide_index=True
    )