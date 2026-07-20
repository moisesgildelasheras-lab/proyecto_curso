"""
Pruebas unitarias para los módulos de carga y auditoría de datos.
"""

import pytest
import pandas as pd
from src.data import load_titanic_data, load_madrid_data, audit_dataset


def test_load_titanic_data():
    """Verifica que el dataset de Titanic se cargue correctamente."""
    df = load_titanic_data("data/Titanic-Dataset.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Survived" in df.columns


def test_load_madrid_data():
    """Verifica que el dataset de Madrid convierta el precio a formato numérico."""
    df = load_madrid_data("data/listings.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "price" in df.columns
    assert pd.api.types.is_numeric_dtype(df["price"])


def test_audit_dataset():
    """Valida el cálculo de métricas de auditoría sobre un DataFrame de prueba."""
    dummy_df = pd.DataFrame({
        "A": [1, 2, None],
        "B": ["x", "y", "z"]
    })
    metrics = audit_dataset(dummy_df)
    
    assert metrics["rows"] == 3
    assert metrics["columns"] == 2
    assert metrics["total_missing"] == 1
    assert metrics["duplicates"] == 0