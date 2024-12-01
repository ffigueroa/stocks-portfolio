import unittest
from typing import cast

from classes.portfolio import Portfolio
from models.portfolio import PortfolioResult


class TestPortfolio(unittest.TestCase):
    """Tests básicos para la clase Portfolio."""

    def test_portfolio_creation(self) -> None:
        """Test de creación de portfolio vacío."""
        portfolio = Portfolio()
        self.assertEqual(len(portfolio.stocks), 0)

    def test_add_stock(self) -> None:
        """Test de agregar una acción al portfolio."""
        portfolio = Portfolio()
        portfolio.add_stock("AAPL", "2023-01-17")

        self.assertEqual(len(portfolio.stocks), 1)
        self.assertEqual(portfolio.stocks[0].symbol, "AAPL")
        self.assertGreater(portfolio.stocks[0].purchase_price, 0)

    def test_portfolio_profit(self) -> None:
        """Test de cálculo de beneficio del portfolio."""
        portfolio = Portfolio()
        portfolio.add_stock("AAPL", "2023-01-17")
        portfolio.add_stock("MSFT", "2023-01-17")

        result = cast(PortfolioResult, portfolio.profit("2023-01-17", "2023-01-18"))

        # Verificamos que los valores son coherentes
        self.assertEqual(len(result["stocks"]), 2)
        self.assertGreater(result["total_investment"], 0)
        total_profit = sum(stock["profit"] for stock in result["stocks"])
        self.assertEqual(result["total_profit"], total_profit)


if __name__ == "__main__":
    unittest.main()
