"""
Aplicación Principal — Streamlit Data Studio
Punto de entrada de la aplicación.
"""

import streamlit as st
from src.styles import apply_custom_styles
from pathlib import Path

st.set_page_config(
    page_title="Streamlit Data Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

# Banner Principal (Corregido st.subtitle -> st.caption / markdown)
st.title("🚀 Streamlit Data Studio")
st.caption("Plataforma Modular de Análisis Exploratorio y Diagnóstico de Datos")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        ### ¡Bienvenido/a al Panel de Control!
        
        Esta aplicación ha sido diseñada siguiendo una arquitectura modular de software, 
        optimizada para la auditoría, análisis estadístico y visualización interactiva de datos.

        #### 📌 Módulos Disponibles:
        
        1. **🔍 0_Diagnostico:** Auditoría completa de calidad del dato, presencia de nulos y estadísticas descriptivas para Titanic y Madrid.
        2. **🚢 1_Titanic:** Análisis interactivo de supervivencia, tarifas y distribución socioeconómica de los pasajeros.
        3. **🏠 2_Madrid:** Exploratorio de oferta turística, precios por distrito y mapa interactivo de alojamientos.
        4. **📊 3_Galeria:** Comparativas avanzadas, gráficos interactivos y matriz de correlaciones.
        """
    )

with col2:
    st.info(
        """
        ### 🛠️ Detalles del Proyecto
        * **Arquitectura:** Modular (`src/`)
        * **Framework:** Streamlit + Pandas + Plotly
        * **Data Cleanliness:** Integrada
        * **Estado:** Sprint 2 Completado
        """
    )

st.divider()

# Botón de acceso directo
# Opción 1: Sintaxis estándar relativa de Streamlit
if st.button("🔍 Comenzar explorando la Auditoría de Datos", type="primary", use_container_width=True):
    st.switch_page("pages/0_Diagnostico.py")