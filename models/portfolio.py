"""Portfolio model definitions."""

from typing import List, TypedDict

from .stock import StockResult


class PortfolioResult(TypedDict):
    """Result of a portfolio profit calculation."""

    stocks: List[StockResult]
    total_investment: float
    total_profit: float
    annualized_return: float
