"""Módulo que implementa la clase Portfolio para gestionar colecciones de acciones."""

from datetime import datetime
from typing import List, Tuple

from dateutil.relativedelta import relativedelta

from classes.stock import Stock
from custom_types import PortfolioResult, StockResult


class Portfolio:
    """Gestiona una colección de acciones y calcula métricas del portfolio."""

    def __init__(self) -> None:
        """Inicializa un portfolio vacío."""
        self.stocks: List[Stock] = []

    def add_stock(self, symbol: str, purchase_date: str) -> None:
        """
        Agrega una acción al portfolio.

        Args:
            symbol: Símbolo de la acción (ej: AAPL)
            purchase_date: Fecha de compra en formato YYYY-MM-DD

        Raises:
            ValueError: Si el símbolo es inválido o no hay datos disponibles
        """
        stock = Stock(symbol, purchase_date)
        self.stocks.append(stock)

    def _validate_dates(self, start_date: str, end_date: str) -> Tuple[datetime, datetime]:
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

    def profit(self, start_date: str, end_date: str) -> PortfolioResult:
        """
        Calcula el beneficio y métricas del portfolio entre dos fechas.

        Args:
            start_date: Fecha inicial en formato YYYY-MM-DD
            end_date: Fecha final en formato YYYY-MM-DD

        Returns:
            PortfolioResult: Diccionario con los resultados del cálculo:
                - stocks: Lista de diccionarios con información de cada acción
                - total_investment: Inversión total realizada
                - total_profit: Beneficio total
                - annualized_return: Retorno anualizado

        Raises:
            ValueError: Si las fechas son inválidas o no hay datos disponibles
        """
        if not self.stocks:
            return {
                "stocks": [],
                "total_investment": 0.0,
                "total_profit": 0.0,
                "annualized_return": 0.0,
            }

        # Validar fechas
        start, end = self._validate_dates(start_date, end_date)

        # Calcular beneficios
        total_investment = 0.0
        total_profit = 0.0
        stocks_data: List[StockResult] = []

        for stock in self.stocks:
            result = stock.calculate_profit(end_date)
            total_investment += result["purchase_price"]
            total_profit += result["profit"]
            stocks_data.append(result)

        # Calcular retorno anualizado
        if total_investment > 0:
            # Calcular años transcurridos con precisión
            years = (
                relativedelta(end, start).years
                + relativedelta(end, start).months / 12.0
                + relativedelta(end, start).days / 365.0
            )

            if years > 0:
                annualized_return = ((1 + total_profit / total_investment) ** (1 / years)) - 1
            else:
                annualized_return = total_profit / total_investment
        else:
            annualized_return = 0.0

        return {
            "stocks": stocks_data,
            "total_investment": total_investment,
            "total_profit": total_profit,
            "annualized_return": annualized_return,
        }
