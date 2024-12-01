"""Utilidades de datos de mercado para operaciones con acciones."""

from datetime import datetime, timedelta
from typing import Optional, Tuple

import pandas as pd
import yfinance as yf  # type: ignore


def get_ticker(symbol: str) -> yf.Ticker:
    """Obtiene un ticker para el símbolo especificado."""
    return yf.Ticker(symbol)


def get_stock_history(
    symbol: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    period: Optional[str] = None,
) -> pd.DataFrame:
    """Obtiene el historial de precios de una acción."""
    ticker = get_ticker(symbol)
    if period:
        history: pd.DataFrame = ticker.history(period=period)
        return history
    if start is None:
        raise ValueError("Debe especificar start o period")
    history = ticker.history(start=start, end=end or start + timedelta(days=1), interval="1d")
    return history


def get_stock_price(symbol: str, date: datetime) -> float:
    """Obtiene el precio de cierre de una acción para una fecha específica."""
    try:
        # Intentamos obtener el precio para la fecha específica
        hist = get_stock_history(symbol, start=date)
        if len(hist) > 0:
            return float(hist["Close"].iloc[0])

        # Si no hay datos para esa fecha, buscamos el último precio disponible
        # Buscamos hasta 10 días antes para encontrar el último precio
        hist = get_stock_history(symbol, start=date - timedelta(days=10), end=date)
        if len(hist) > 0:
            return float(hist["Close"].iloc[-1])  # Tomamos el último precio disponible

        raise ValueError(f"No se encontraron datos históricos para {symbol}")
    except Exception as e:
        raise ValueError(f"Error al obtener el precio para {symbol}: {str(e)}")


def is_trading_day(symbol: str, date: datetime) -> bool:
    """Verifica si una fecha es un día de trading para una acción."""
    try:
        hist = get_stock_history(symbol, start=date)
        return len(hist) > 0
    except Exception:
        return False


def get_next_trading_day(symbol: str, date: datetime, max_attempts: int = 10) -> datetime:
    """Obtiene el siguiente día de trading disponible."""
    next_day = date
    attempts = 0

    while not is_trading_day(symbol, next_day) and attempts < max_attempts:
        next_day += timedelta(days=1)
        attempts += 1

    if attempts >= max_attempts:
        raise ValueError(f"No se encontró día de trading después de {date} para {symbol}")

    return next_day


def validate_symbol(symbol: str) -> None:
    """Valida si un símbolo existe y tiene datos disponibles."""
    try:
        hist = get_stock_history(symbol, period="5d")

        if hist.empty:
            raise ValueError(f"No se encontraron datos históricos para {symbol}")

        last_price = hist["Close"].iloc[-1]
        if pd.isna(last_price) or last_price <= 0:
            raise ValueError(f"Precio inválido para {symbol}")

    except Exception as e:
        raise ValueError(f"Error al validar {symbol}: {str(e)}")

def validate_dates(start_date: str, end_date: str) -> Tuple[datetime, datetime]:
    """
    Valida y convierte las fechas.

    Args:
        start_date: Fecha inicial en formato YYYY-MM-DD
        end_date: Fecha final en formato YYYY-MM-DD

    Returns:
        tuple: (fecha_inicial, fecha_final) como objetos datetime

    Raises:
        ValueError: Si las fechas son inválidas
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Las fechas deben estar en formato YYYY-MM-DD")

    if end < start:
        raise ValueError("La fecha final debe ser posterior a la inicial")

    return start, end


def calculate_years_between(start: datetime, end: datetime) -> float:
    """
    Calcula los años transcurridos entre dos fechas.

    Args:
        start: Fecha inicial
        end: Fecha final

    Returns:
        float: Años transcurridos (puede ser fracción)
    """
    # Calculamos la diferencia en días
    delta = end - start
    return max(delta.days / 365.25, 0.003)  # Mínimo ~1 día en años