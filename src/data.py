"""
Módulo de carga, validación y preparación de datos.
Se encarga de leer los CSVs y calcular métricas de diagnóstico.
"""

import pandas as pd
import streamlit as st
from typing import Tuple, Dict, Any


@st.cache_data
def load_titanic_data(filepath: str = "data/Titanic-Dataset.csv") -> pd.DataFrame:
    """
    Carga y realiza una limpieza inicial básica del dataset de Titanic.
    """
    df = pd.read_csv(filepath)
    # Asegurar tipos adecuados si fuera necesario
    df['PassengerId'] = df['PassengerId'].astype(int)
    return df


@st.cache_data
def load_madrid_data(filepath: str = "data/listings.csv") -> pd.DataFrame:
    """
    Carga y realiza una limpieza inicial básica del dataset de Madrid.
    """
    df = pd.read_csv(filepath)
    # Garantizar que el precio sea numérico (float)
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    return df


def audit_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula métricas clave de diagnóstico sobre un DataFrame.
    """
    num_rows, num_cols = df.shape
    missing_sum = df.isnull().sum()
    total_missing = missing_sum.sum()
    total_cells = num_rows * num_cols
    
    return {
        "shape": df.shape,
        "rows": num_rows,
        "columns": num_cols,
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 ** 2), 2),
        "duplicates": df.duplicated().sum(),
        "missing_by_col": missing_sum,
        "total_missing": total_missing,
        "missing_pct": round((total_missing / total_cells) * 100, 2) if total_cells > 0 else 0,
        "dtypes": df.dtypes
    }