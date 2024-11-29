"""Ejemplo de uso del portfolio de stocks."""

import logging
from typing import List, Tuple

from classes.portfolio import Portfolio, PortfolioResult
from utils.market_utils import format_currency, format_percentage, print_logo, print_stock_info

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Función principal que demuestra el uso del portfolio."""
    try:
        print_logo()
        # Crear portfolio
        portfolio = Portfolio()
        logger.info("Portfolio creado")

        # Acciones a agregar: símbolo y fecha de compra
        stocks_to_add: List[Tuple[str, str]] = [
            ("AAPL", "2023-01-14"),  # Sábado - se moverá al siguiente día hábil
            ("MSFT", "2023-06-01"),  # Jueves - día hábil
            ("GOOGL", "2023-09-17"),  # Domingo - se moverá al siguiente día hábil
        ]

        # Agregar acciones al portfolio
        for symbol, purchase_date in stocks_to_add:
            try:
                logger.info(f"\nIntentando agregar {symbol} con fecha {purchase_date}")
                portfolio.add_stock(symbol, purchase_date)
            except ValueError as e:
                logger.error(f"✗ Error: {str(e)}")
                continue

        # Definir período de análisis
        start_date = "2023-01-01"
        end_date = "2024-10-25"

        # Calcular beneficios
        result: PortfolioResult = portfolio.profit(start_date, end_date)

        # Mostrar resultados por acción
        logger.info(f"\nStocks del portfolio al {end_date}:")
        for stock in result["stocks"]:
            print_stock_info(stock)

        # Mostrar resumen del portfolio
        current_value = result["total_investment"] + result["total_profit"]
        logger.info("\nResumen del Portfolio:")
        logger.info(f"Inversión total: {format_currency(result['total_investment'])}")
        logger.info(f"Valor actual: {format_currency(current_value)}")
        logger.info(f"Beneficio total: {format_currency(result['total_profit'])}")
        logger.info(f"Retorno anualizado: {format_percentage(result['annualized_return']*100)}")

    except Exception as e:
        logger.error(f"\nError inesperado: {str(e)}")
        raise


if __name__ == "__main__":
    main()
