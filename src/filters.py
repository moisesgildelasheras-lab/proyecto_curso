"""
Módulo de Gestión Centralizada de Filtros.

Este archivo se encarga de:
1. Renderizar la interfaz de usuario de los filtros en la barra lateral (Sidebar).
2. Mantener y sincronizar el estado global mediante Streamlit Session State.
3. Aplicar las transformaciones y filtrados sobre los DataFrames correspondientes.
"""

import pandas as pd
import streamlit as st
from typing import Tuple


def init_session_state():
    """
    Inicializa las variables del Session State si no existen previamente.
    Garantiza la persistencia de los filtros al navegar entre páginas.
    """
    # Estado para Titanic
    if "titanic_pclass" not in st.session_state:
        st.session_state.titanic_pclass = ["Todas", "1ª Clase", "2ª Clase", "3ª Clase"]
    if "titanic_sex" not in st.session_state:
        st.session_state.titanic_sex = ["Todos", "male", "female"]
    if "titanic_age_range" not in st.session_state:
        st.session_state.titanic_age_range = (0, 80)

    # Estado para Madrid
    if "madrid_room_types" not in st.session_state:
        st.session_state.madrid_room_types = []
    if "madrid_neighbourhoods" not in st.session_state:
        st.session_state.madrid_neighbourhoods = []
    if "madrid_price_range" not in st.session_state:
        st.session_state.madrid_price_range = (0.0, 1000.0)


# ==========================================================
# FILTROS DE TITANIC
# ==========================================================

def render_titanic_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza los filtros de Titanic en el Sidebar y retorna el DataFrame filtrado.

    Parameters:
        df (pd.DataFrame): Dataset original de Titanic.

    Returns:
        pd.DataFrame: Dataset filtrado según las selecciones del usuario.
    """
    st.sidebar.header("🚢 Filtros Titanic")

    # Copia defensiva del DataFrame
    df_filtered = df.copy()

    # 1. Filtro por Clase (Pclass)
    classes_available = sorted(df['Pclass'].dropna().unique().tolist())
    class_options = ["Todas"] + [f"{c}ª Clase" for c in classes_available]
    
    selected_class = st.sidebar.selectbox(
        "Clase del Pasajero:",
        options=class_options,
        index=0,
        help="Selecciona una clase específica o 'Todas' para incluir todo el pasaje."
    )

    # 2. Filtro por Sexo (Sex)
    sex_options = ["Todos", "male", "female"]
    selected_sex = st.sidebar.radio(
        "Género / Sexo:",
        options=sex_options,
        index=0,
        horizontal=True
    )

    # 3. Filtro por Rango de Edad (Age)
    min_age = int(df['Age'].min()) if not pd.isna(df['Age'].min()) else 0
    max_age = int(df['Age'].max()) if not pd.isna(df['Age'].max()) else 80

    selected_age = st.sidebar.slider(
        "Rango de Edad:",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
        step=1
    )

    # 4. Filtro por Puerto de Embarque (Embarked)
    embarked_map = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}
    embarked_options = ["Todos"] + [embarked_map.get(e, e) for e in df['Embarked'].dropna().unique()]
    
    selected_embarked = st.sidebar.selectbox(
        "Puerto de Embarque:",
        options=embarked_options,
        index=0
    )

    # Botón para resetear filtros
    if st.sidebar.button("🔄 Restablecer Filtros Titanic", use_container_width=True):
        st.rerun()

    # --- LÓGICA DE FILTRADO ---
    if selected_class != "Todas":
        pclass_num = int(selected_class.split("ª")[0])
        df_filtered = df_filtered[df_filtered['Pclass'] == pclass_num]

    if selected_sex != "Todos":
        df_filtered = df_filtered[df_filtered['Sex'] == selected_sex]

    # Incluir pasajeros dentro del rango de edad (conservando nulos para no perderlos salvo filtrado estricto)
    df_filtered = df_filtered[
        (df_filtered['Age'].between(selected_age[0], selected_age[1])) | (df_filtered['Age'].isna())
    ]

    if selected_embarked != "Todos":
        reverse_map = {v: k for k, v in embarked_map.items()}
        code = reverse_map.get(selected_embarked, selected_embarked)
        df_filtered = df_filtered[df_filtered['Embarked'] == code]

    st.sidebar.caption(f"📍 Registros mostrados: **{len(df_filtered)}** de **{len(df)}**")
    return df_filtered


# ==========================================================
# FILTROS DE MADRID
# ==========================================================

def render_madrid_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza los filtros de Madrid Listings en el Sidebar y retorna el DataFrame filtrado.

    Parameters:
        df (pd.DataFrame): Dataset original de Madrid.

    Returns:
        pd.DataFrame: Dataset filtrado según las selecciones del usuario.
    """
    st.sidebar.header("🏠 Filtros Madrid Airbnb")

    # Copia defensiva
    df_filtered = df.copy()

    # 1. Filtro por Grupo de Barrio (neighbourhood_group)
    groups = sorted(df['neighbourhood_group'].dropna().unique().tolist())
    selected_groups = st.sidebar.multiselect(
        "Distrito / Grupo de Barrio:",
        options=groups,
        default=[],
        placeholder="Todos los distritos"
    )

    # 2. Filtro por Tipo de Habitación (room_type)
    room_types = sorted(df['room_type'].dropna().unique().tolist())
    selected_room_types = st.sidebar.multiselect(
        "Tipo de Alojamiento:",
        options=room_types,
        default=[],
        placeholder="Todos los tipos"
    )

    # 3. Filtro por Rango de Precio por Noche (price)
    min_price = float(df['price'].min()) if not pd.isna(df['price'].min()) else 0.0
    max_price = float(df['price'].max()) if not pd.isna(df['price'].max()) else 1000.0

    selected_price = st.sidebar.slider(
        "Precio por Noche (€):",
        min_value=0.0,
        max_value=min(max_price, 2000.0),  # Acotado para evitar deformación por outliers
        value=(min_price, min(max_price, 500.0)),
        step=5.0
    )

    # 4. Filtro por Número Mínimo de Reseñas
    min_reviews = st.sidebar.number_input(
        "Mínimo de Reseñas acumuladas:",
        min_value=0,
        max_value=int(df['number_of_reviews'].max()),
        value=0,
        step=5
    )

    # Botón para resetear filtros
    if st.sidebar.button("🔄 Restablecer Filtros Madrid", use_container_width=True):
        st.rerun()

    # --- LÓGICA DE FILTRADO ---
    if selected_groups:
        df_filtered = df_filtered[df_filtered['neighbourhood_group'].isin(selected_groups)]

    if selected_room_types:
        df_filtered = df_filtered[df_filtered['room_type'].isin(selected_room_types)]

    df_filtered = df_filtered[
        df_filtered['price'].between(selected_price[0], selected_price[1])
    ]

    if min_reviews > 0:
        df_filtered = df_filtered[df_filtered['number_of_reviews'] >= min_reviews]

    st.sidebar.caption(f"📍 Alojamientos mostrados: **{len(df_filtered):,}** de **{len(df):,}**")
    return df_filtered