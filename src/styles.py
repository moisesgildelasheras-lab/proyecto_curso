"""
Configuración visual, constantes estéticas e inyección de CSS.
"""

import streamlit as st

# Paleta de colores principal
PRIMARY_COLOR = "#0066CC"
BACKGROUND_COLOR = "#F8F9FA"
ACCENT_COLOR = "#FF4B4B"

def apply_custom_styles():
    """
    Aplica estilos personalizados mediante CSS inyectado en Streamlit.
    """
    custom_css = """
    <style>
        /* Ajuste de margen superior general */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Estilo para tarjetas / contenedores de KPIs */
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)