"""Módulo que implementa la clase Stock para gestionar acciones individuales."""

import pandas as pd

from models.stock import StockResult
from utils.market import (
    calculate_annualized_return,
    calculate_years_between,
    get_next_trading_day,
    get_stock_price,
    validate_symbol,
)


class Stock:
    """Representa una acción con su fecha de compra y precio."""

    def __init__(self, symbol: str, purchase_date: str) -> None:
        """
        Inicializa una acción.

        Args:
            symbol: Símbolo de la acción (ej: AAPL)
            purchase_date: Fecha de compra en formato YYYY-MM-DD

        Raises:
            ValueError: Si el símbolo es inválido o no hay datos disponibles
        """
        # Convertimos el símbolo a mayúsculas y validamos
        self.symbol = symbol.upper()
        validate_symbol(self.symbol)

        # Convertimos la fecha de compra
        self.purchase_date = pd.to_datetime(purchase_date).to_pydatetime()

        # Ajustamos la fecha si es necesario
        next_business_day = get_next_trading_day(self.symbol, self.purchase_date)
        if next_business_day != self.purchase_date:
            print(
                f"Nota: La compra de {self.symbol} se ejecutará el {next_business_day} "
                f"(siguiente día hábil después de {self.purchase_date})"
            )
            self.purchase_date = next_business_day

        # Obtenemos el precio de compra
        self.purchase_price = get_stock_price(self.symbol, self.purchase_date)

    def calculate_profit(self, end_date: str) -> StockResult:
        """
        Calcula el beneficio de la acción hasta una fecha específica.

        Args:
            end_date: Fecha final en formato YYYY-MM-DD

        Returns:
            StockResult: Información sobre la acción y su beneficio
        """
        end_datetime = pd.to_datetime(end_date).to_pydatetime()
        end_price = get_stock_price(self.symbol, end_datetime)
        profit = end_price - self.purchase_price

        # Calcular retorno anualizado
        years = calculate_years_between(self.purchase_date, end_datetime)
        total_return = profit / self.purchase_price
        annualized_return = calculate_annualized_return(total_return, years)

        return {
            "symbol": self.symbol,
            "purchase_date": self.purchase_date,
            "purchase_price": self.purchase_price,
            "end_price": end_price,
            "profit": profit,
            "annualized_return": annualized_return,
        }
