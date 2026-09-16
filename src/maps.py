
"""
Visualizaciones geográficas para el dataset de Madrid Listings.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_madrid_map(df: pd.DataFrame) -> go.Figure:
    if df.empty or 'latitude' not in df.columns or 'longitude' not in df.columns:
        fig = go.Figure()
        fig.update_layout(
            title="Sin datos geográficos disponibles",
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig

    # 1. Filtrar nulos y asegurar tipo numérico
    df_map = df.dropna(subset=['latitude', 'longitude', 'price']).copy()
    df_map['price'] = pd.to_numeric(df_map['price'], errors='coerce')
    df_map = df_map.dropna(subset=['price'])

    # 2. Filtrar coordenadas válidas de la Comunidad de Madrid
    df_map = df_map[
        (df_map['latitude'].between(40.0, 41.0)) & 
        (df_map['longitude'].between(-4.5, -3.0))
    ]

    if df_map.empty:
        fig = go.Figure()
        fig.update_layout(title="No hay coordenadas válidas dentro de Madrid")
        return fig

    # 3. Limitar el rango de color para evitar el sesgo de precios extremos
    max_color_price = min(df_map['price'].quantile(0.95), 300.0)

    # 4. Crear el mapa especificando el centro
    fig = px.scatter_map(
        df_map,
        lat="latitude",
        lon="longitude",
        color="price",
        color_continuous_scale="Viridis",
        range_color=(df_map['price'].min(), max_color_price),
        zoom=11,
        center={"lat": 40.416775, "lon": -3.703790},  # Puerta del Sol (Madrid)
        map_style="open-street-map",
        hover_name="name",
        title="<b>Distribución Geográfica de Alojamientos en Madrid</b>"
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        template="plotly_white"
    )

    return fig
