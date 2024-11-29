"""Tipos compartidos para el proyecto."""

from datetime import datetime
from typing import List, TypedDict


class StockResult(TypedDict):
    """Tipo para el resultado del cálculo de beneficio."""

    symbol: str
    purchase_date: datetime
    purchase_price: float
    end_price: float
    profit: float


class PortfolioResult(TypedDict):
    """Tipo para el resultado del cálculo de beneficio del portfolio."""

    stocks: List[StockResult]
    total_investment: float
    total_profit: float
    annualized_return: float
