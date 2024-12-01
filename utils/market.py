"""Market data utilities for stock operations."""

from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import yfinance as yf  # type: ignore


def get_ticker(symbol: str) -> yf.Ticker:
    """Get a Ticker object for the specified symbol."""
    return yf.Ticker(symbol)


def get_stock_history(
    symbol: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    period: Optional[str] = None,
) -> pd.DataFrame:
    """Get stock price history."""
    ticker = get_ticker(symbol)
    if period:
        history: pd.DataFrame = ticker.history(period=period)
        return history
    if start is None:
        raise ValueError("Must specify start or period")
    history = ticker.history(start=start, end=end or start + timedelta(days=1), interval="1d")
    return history


def get_stock_price(symbol: str, date: datetime) -> float:
    """Get stock closing price for a specific date."""
    try:
        hist = get_stock_history(symbol, start=date)
        if len(hist) == 0:
            raise ValueError(f"No data available for {symbol} on {date}")
        return float(hist["Close"].iloc[0])
    except Exception as e:
        raise ValueError(f"Error getting price for {symbol}: {str(e)}")


def is_trading_day(symbol: str, date: datetime) -> bool:
    """Check if a date is a trading day for a stock."""
    try:
        hist = get_stock_history(symbol, start=date)
        return len(hist) > 0
    except Exception:
        return False


def get_next_trading_day(symbol: str, date: datetime, max_attempts: int = 10) -> datetime:
    """Get the next available trading day."""
    next_day = date
    attempts = 0

    while not is_trading_day(symbol, next_day) and attempts < max_attempts:
        next_day += timedelta(days=1)
        attempts += 1

    if attempts >= max_attempts:
        raise ValueError(f"No trading day found after {date} for {symbol}")

    return next_day


def validate_symbol(symbol: str) -> None:
    """Validate if a symbol exists and has available data."""
    try:
        hist = get_stock_history(symbol, period="5d")

        if hist.empty:
            raise ValueError(f"No historical data found for {symbol}")

        last_price = hist["Close"].iloc[-1]
        if pd.isna(last_price) or last_price <= 0:
            raise ValueError(f"Invalid price for {symbol}")

    except Exception as e:
        raise ValueError(f"Error validating {symbol}: {str(e)}")
