
"""
Visualizaciones geográficas para el dataset de Madrid Listings.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_madrid_map(df: pd.DataFrame) -> go.Figure:
    """
    Genera un mapa de dispersión interactivo sobre Madrid usando Plotly Express.
    """

    if df.empty or 'latitude' not in df.columns or 'longitude' not in df.columns:
        fig = go.Figure()
        fig.update_layout(
            title="Sin datos geográficos disponibles",
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig

    # Filtrar nulos
    df_map = df.dropna(
        subset=['latitude', 'longitude', 'price']
    ).copy()

    # Asegurar que el precio sea numérico
    df_map['price'] = pd.to_numeric(
        df_map['price'],
        errors='coerce'
    )

    df_map = df_map.dropna(subset=['price'])

    # Escala de color basada en el rango real de precios
    min_price = df_map['price'].min()
    max_price = df_map['price'].max()

    fig = px.scatter_map(
        df_map,
        lat="latitude",
        lon="longitude",
        color="price",
        color_continuous_scale="Viridis",
        range_color=(min_price, max_price),
        size_max=10,
        zoom=10,
        map_style="open-street-map",
        hover_name="name",
        hover_data={
            "price": ":.2f €",
            "room_type": True,
            "neighbourhood_group": True,
            "number_of_reviews": True,
            "latitude": False,
            "longitude": False
        },
        title="<b>Distribución Geográfica de Alojamientos en Madrid</b>",
        labels={"price": "Precio (€)"}
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        template="plotly_white"
    )

    return fig

