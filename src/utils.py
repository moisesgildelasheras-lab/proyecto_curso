"""
Funciones auxiliares y formateadores reutilizables.
"""

def format_currency(value: float, currency_symbol: str = "€") -> str:
    """
    Formatea un número flotante como moneda.
    """
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.2f} {currency_symbol}".replace(",", " ")


def format_percentage(value: float) -> str:
    """
    Formatea un valor decimal a porcentaje.
    """
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value * 100:.1f}%"