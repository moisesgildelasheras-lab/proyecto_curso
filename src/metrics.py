"""
Cálculo centralizado de KPIs e indicadores estadísticos.
"""

import pandas as pd
from typing import Dict, Any


def get_titanic_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula los KPIs clave para el conjunto de datos de Titanic.

    Parameters:
        df (pd.DataFrame): DataFrame del Titanic (filtrado o completo).

    Returns:
        Dict[str, Any]: Diccionario con métricas agregadas.
    """
    total_passengers = len(df)
    
    if total_passengers == 0:
        return {
            "total_passengers": 0,
            "survivors": 0,
            "survival_rate": 0.0,
            "avg_age": 0.0,
            "avg_fare": 0.0,
            "median_fare": 0.0
        }

    survivors = int(df['Survived'].sum())
    survival_rate = round((survivors / total_passengers) * 100, 2)
    avg_age = round(df['Age'].mean(), 1) if not df['Age'].dropna().empty else 0.0
    avg_fare = round(df['Fare'].mean(), 2) if not df['Fare'].dropna().empty else 0.0
    median_fare = round(df['Fare'].median(), 2) if not df['Fare'].dropna().empty else 0.0

    return {
        "total_passengers": total_passengers,
        "survivors": survivors,
        "survival_rate": survival_rate,
        "avg_age": avg_age,
        "avg_fare": avg_fare,
        "median_fare": median_fare
    }


def get_madrid_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula los KPIs clave para el conjunto de datos de Madrid Listings.

    Parameters:
        df (pd.DataFrame): DataFrame de Madrid (filtrado o completo).

    Returns:
        Dict[str, Any]: Diccionario con métricas agregadas.
    """
    total_listings = len(df)

    if total_listings == 0:
        return {
            "total_listings": 0,
            "avg_price": 0.0,
            "median_price": 0.0,
            "avg_availability": 0,
            "total_reviews": 0
        }

    valid_prices = df['price'].dropna()
    avg_price = round(valid_prices.mean(), 2) if not valid_prices.empty else 0.0
    median_price = round(valid_prices.median(), 2) if not valid_prices.empty else 0.0
    
    avg_availability = round(df['availability_365'].mean(), 0) if 'availability_365' in df.columns else 0
    total_reviews = int(df['number_of_reviews'].sum()) if 'number_of_reviews' in df.columns else 0

    return {
        "total_listings": total_listings,
        "avg_price": avg_price,
        "median_price": median_price,
        "avg_availability": int(avg_availability),
        "total_reviews": total_reviews
    }