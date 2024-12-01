"""Stock model definitions."""

from datetime import datetime
from typing import TypedDict


class StockResult(TypedDict):
    """Result of a stock profit calculation."""

    symbol: str
    purchase_date: datetime
    purchase_price: float
    end_price: float
    profit: float
