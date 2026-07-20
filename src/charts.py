"""
Funciones para la generación desacoplada de visualizaciones con Plotly.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_survival_by_class(df: pd.DataFrame) -> go.Figure:
    """
    Genera un gráfico de barras agrupadas de Supervivencia por Clase.
    """
    if df.empty:
        return px.bar(title="Sin datos para mostrar")

    # Mapeo de supervivencia
    df_plot = df.copy()
    df_plot['Estado'] = df_plot['Survived'].map({0: 'Fallecido', 1: 'Superviviente'})
    df_plot['Clase'] = df_plot['Pclass'].map({1: '1ª Clase', 2: '2ª Clase', 3: '3ª Clase'})

    grouped = df_plot.groupby(['Clase', 'Estado']).size().reset_index(name='Pasajeros')

    fig = px.bar(
        grouped,
        x='Clase',
        y='Pasajeros',
        color='Estado',
        barmode='group',
        color_discrete_map={'Superviviente': '#2ECC71', 'Fallecido': '#E74C3C'},
        title="<b>Supervivencia por Clase de Pasajero</b>",
        labels={'Pasajeros': 'Número de Pasajeros', 'Clase': ''}
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    return fig


def plot_age_distribution_by_survival(df: pd.DataFrame) -> go.Figure:
    """
    Genera un histograma/densidad de la distribución de edad por supervivencia.
    """
    if df.empty:
        return px.histogram(title="Sin datos para mostrar")

    df_plot = df.dropna(subset=['Age']).copy()
    df_plot['Estado'] = df_plot['Survived'].map({0: 'Fallecido', 1: 'Superviviente'})

    fig = px.histogram(
        df_plot,
        x='Age',
        color='Estado',
        nbins=30,
        opacity=0.7,
        barmode='overlay',
        color_discrete_map={'Superviviente': '#2ECC71', 'Fallecido': '#E74C3C'},
        title="<b>Distribución de Edad según Supervivencia</b>",
        labels={'Age': 'Edad (Años)', 'count': 'Frecuencia'}
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    return fig


def plot_fare_vs_age_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Genera un gráfico de dispersión de Tarifa vs. Edad segmentado por Sexo y Estado.
    """
    if df.empty:
        return px.scatter(title="Sin datos para mostrar")

    df_plot = df.dropna(subset=['Age', 'Fare']).copy()
    df_plot['Estado'] = df_plot['Survived'].map({0: 'Fallecido', 1: 'Superviviente'})

    fig = px.scatter(
        df_plot,
        x='Age',
        y='Fare',
        color='Estado',
        size='Pclass',
        hover_data=['Name', 'Ticket'],
        color_discrete_map={'Superviviente': '#2ECC71', 'Fallecido': '#E74C3C'},
        title="<b>Relación Tarifa (€) vs. Edad por Estado de Supervivencia</b>",
        labels={'Age': 'Edad', 'Fare': 'Tarifa (€)'}
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    return fig


def plot_embarked_pie(df: pd.DataFrame) -> go.Figure:
    """
    Genera un gráfico de tarta con la distribución por Puerto de Embarque.
    """
    if df.empty:
        return px.pie(title="Sin datos para mostrar")

    df_plot = df.copy()
    embarked_map = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}
    df_plot['Puerto'] = df_plot['Embarked'].map(embarked_map).fillna('Desconocido')

    grouped = df_plot['Puerto'].value_counts().reset_index()
    grouped.columns = ['Puerto', 'Cantidad']

    fig = px.pie(
        grouped,
        names='Puerto',
        values='Cantidad',
        hole=0.4,
        title="<b>Distribución por Puerto de Embarque</b>",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    return fig

def plot_price_by_neighbourhood(df: pd.DataFrame) -> go.Figure:
    """
    Genera un gráfico de barras horizonal del precio medio por Distrito.
    """
    if df.empty or 'neighbourhood_group' not in df.columns:
        return px.bar(title="Sin datos para mostrar")

    grouped = (
        df.groupby('neighbourhood_group')['price']
        .mean()
        .reset_index()
        .sort_values(by='price', ascending=True)
    )

    fig = px.bar(
        grouped,
        x='price',
        y='neighbourhood_group',
        orientation='h',
        color='price',
        color_continuous_scale='Blues',
        title="<b>Precio Medio por Distrito / Grupo de Barrio (€)</b>",
        labels={'price': 'Precio Medio (€)', 'neighbourhood_group': 'Distrito'}
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    return fig


def plot_room_type_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Genera un gráfico de donut con la distribución por tipo de alojamiento.
    """
    if df.empty or 'room_type' not in df.columns:
        return px.pie(title="Sin datos para mostrar")

    grouped = df['room_type'].value_counts().reset_index()
    grouped.columns = ['Tipo', 'Cantidad']

    fig = px.pie(
        grouped,
        names='Tipo',
        values='Cantidad',
        hole=0.4,
        title="<b>Distribución por Tipo de Alojamiento</b>",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    return fig