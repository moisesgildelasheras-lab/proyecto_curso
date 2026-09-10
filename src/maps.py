"""
Visualizaciones geográficas para el dataset de Madrid Listings.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_madrid_map(df: pd.DataFrame) -> go.Figure:
    """
    Genera un mapa de dispersión interactivo sobre Madrid usando Plotly Express.

    Parameters:
        df (pd.DataFrame): DataFrame filtrado de Madrid con 'latitude', 'longitude' y 'price'.

    Returns:
        go.Figure: Figura de Plotly con la representación geográfica.
    """
    if df.empty or 'latitude' not in df.columns or 'longitude' not in df.columns:
        fig = go.Figure()
        fig.update_layout(
            title="Sin datos geográficos disponibles",
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig

    # Filtrar nulos en coordenadas
    df_map = df.dropna(subset=['latitude', 'longitude', 'price']).copy()

    # Acotar precios para evitar que outliers distorsionen la escala cromática
    q95 = df_map['price'].quantile(0.95) if not df_map.empty else 500
    df_map['price_clipped'] = df_map['price'].clip(upper=q95)

    print(df_map.dtypes)
    print(df_map["price_clipped"].head())

    fig = px.scatter_map(
        df_map,
        lat="latitude",
        lon="longitude",
        color="price_clipped",
        size_max=12,
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=12,
        zoom=10,
        mapbox_style="open-street-map",
        hover_name="name",
        hover_data={
            "price": ":.2f €",
            "room_type": True,
            "neighbourhood_group": True,
            "number_of_reviews": True,
            "price_clipped": False,
            "latitude": False,
            "longitude": False
        },
        title="<b>Distribución Geográfica de Alojamientos en Madrid</b>",
        labels={'price_clipped': 'Precio (€)'}
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        template="plotly_white"
    )
    return fig
