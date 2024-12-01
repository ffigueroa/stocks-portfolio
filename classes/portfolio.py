"""Módulo que implementa la clase Portfolio para gestionar colecciones de acciones."""

from typing import List

from classes.stock import Stock
from models.portfolio import PortfolioResult, StockResult
from utils import calculate_years_between, validate_dates


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
        _, end = validate_dates(start_date, end_date)

        # Calcular beneficios
        total_investment = 0.0
        total_profit = 0.0
        stocks_data: List[StockResult] = []
        weighted_years = 0.0

        for stock in self.stocks:
            result = stock.calculate_profit(end_date)
            total_investment += result["purchase_price"]
            total_profit += result["profit"]
            stocks_data.append(result)
            # Acumular años ponderados por inversión
            years = calculate_years_between(stock.purchase_date, end)
            weighted_years += years * (result["purchase_price"] / total_investment)

        # Calcular retorno anualizado
        if total_investment > 0:
            # Calcular el retorno total
            total_return = total_profit / total_investment

            # Usar el promedio ponderado de años por inversión
            if weighted_years > 0:
                # Fórmula del retorno anualizado: (1 + r)^(1/t) - 1
                # donde r es el retorno total y t es el tiempo en años
                annualized_return = ((1 + total_return) ** (1 / weighted_years)) - 1
            else:
                # Si el período es muy corto, usar el retorno simple
                annualized_return = total_return
        else:
            annualized_return = 0.0

        return {
            "stocks": stocks_data,
            "total_investment": total_investment,
            "total_profit": total_profit,
            "annualized_return": annualized_return,
        }
