"""Módulo que implementa la clase Portfolio para gestionar colecciones de acciones."""

from typing import List

from classes.stock import Stock
from models.portfolio import PortfolioResult, StockResult
from utils.market import (
    calculate_annualized_return,
    calculate_years_between,
    get_stock_price,
    validate_dates,
)


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
        start, end = validate_dates(start_date, end_date)

        # Calcular beneficios
        total_investment = 0.0
        total_profit = 0.0
        stocks_data: List[StockResult] = []
        weighted_years = 0.0

        for stock in self.stocks:
            # Si la acción fue comprada antes de la fecha de inicio,
            # usar el precio de la fecha de inicio como precio de compra
            if stock.purchase_date < start:
                purchase_price = get_stock_price(stock.symbol, start)
                purchase_date = start
                print(
                    f"Nota: Para {stock.symbol}, usando precio de {start_date} "
                    f"(${purchase_price:.2f}) como precio de compra"
                )
            else:
                purchase_price = stock.purchase_price
                purchase_date = stock.purchase_date

            # Obtener precio final
            end_price = get_stock_price(stock.symbol, end)
            profit = end_price - purchase_price

            # Calcular retorno anualizado individual
            years = calculate_years_between(purchase_date, end)
            total_return = profit / purchase_price
            annualized_return = calculate_annualized_return(total_return, years)

            # Acumular totales
            total_investment += purchase_price
            total_profit += profit

            # Guardar resultados
            stocks_data.append(
                {
                    "symbol": stock.symbol,
                    "purchase_date": purchase_date,
                    "purchase_price": purchase_price,
                    "end_price": end_price,
                    "profit": profit,
                    "annualized_return": annualized_return,
                }
            )

            # Acumular años ponderados por inversión
            weighted_years += years * (purchase_price / total_investment)

        # Calcular retorno anualizado del portfolio
        if total_investment > 0:
            total_return = total_profit / total_investment
            annualized_return = calculate_annualized_return(total_return, weighted_years)
        else:
            annualized_return = 0.0

        return {
            "stocks": stocks_data,
            "total_investment": total_investment,
            "total_profit": total_profit,
            "annualized_return": annualized_return,
        }
