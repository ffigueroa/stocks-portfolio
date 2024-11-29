"""Utilidades para el manejo de datos de mercado y formateo."""

import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import yfinance as yf  # type: ignore

from custom_types import StockResult

logger = logging.getLogger(__name__)


def print_stock_info(stock: StockResult) -> None:
    """Imprime la información detallada de una acción."""
    logger.info(f"\n{stock['symbol']}:")
    logger.info(f"  Fecha de compra: {stock['purchase_date']}")
    logger.info(f"  Precio de compra: {format_currency(stock['purchase_price'])}")
    logger.info(f"  Precio actual: {format_currency(stock['end_price'])}")
    logger.info(f"  Beneficio: {format_currency(stock['profit'])}")
    logger.info(f"  Rendimiento: {format_percentage(stock['profit']/stock['purchase_price']*100)}")


def format_currency(amount: float) -> str:
    """Formatea un número como moneda."""
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """Formatea un número como porcentaje."""
    return f"{value:.2f}%"


def get_ticker(symbol: str) -> yf.Ticker:
    """Obtiene un objeto Ticker para el símbolo especificado."""
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
        raise ValueError("Se debe especificar start o period")
    history = ticker.history(start=start, end=end or start + timedelta(days=1), interval="1d")
    return history


def get_stock_price(symbol: str, date: datetime) -> float:
    """Obtiene el precio de cierre de una acción en una fecha específica."""
    try:
        hist = get_stock_history(symbol, start=date)
        if len(hist) == 0:
            raise ValueError(f"No hay datos disponibles para {symbol} en {date}")
        return float(hist["Close"].iloc[0])
    except Exception as e:
        raise ValueError(f"Error al obtener precio de {symbol}: {str(e)}")


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
        raise ValueError(f"No se encontró un día de trading después de {date} para {symbol}")

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
        raise ValueError(f"Error validando {symbol}: {str(e)}")


def print_logo() -> None:
    """Imprime el logo ASCII de la aplicación."""
    logo = """
          :::::::
       ::::::::::::       ::::::::::::::                                               :::
       :::::::::::::      :::       :::               :::                              :::
 :::::::::::::::::::      :::       :::: ::: :::::  :::::::: ::::    :::    :::::::::  :::
 :::::::::::::::::::      ::::::::  :::: :::::::::: :::::::: ::::    :::  :::::::::::: :::
 ::::::::::::::::::       ::::::::  :::: ::::   ::::  :::    ::::    :::  :::     :::: :::
 :::::::::::::::::        :::       :::: :::    ::::  :::    ::::    :::  :::     :::: :::
 ::::::::::               :::       :::: :::    ::::  ::::   :::::  ::::  ::::   ::::: :::
 ::::::::                 :::       :::: :::    ::::   :::::  ::::::::::   ::::::::::: :::
 :::::
    """
    print(logo)
