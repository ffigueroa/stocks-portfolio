"""Tests para la clase Stock."""

import unittest
from typing import cast

from classes.stock import Stock
from custom_types import StockResult


class TestStock(unittest.TestCase):
    """Tests básicos para la clase Stock."""

    def test_stock_creation(self) -> None:
        """Test básico de creación de una acción."""
        stock = Stock("AAPL", "2023-01-17")

        self.assertEqual(stock.symbol, "AAPL")
        self.assertGreater(stock.purchase_price, 0)

    def test_calculate_profit(self) -> None:
        """Test básico de cálculo de beneficio."""
        stock = Stock("AAPL", "2023-01-17")
        result = cast(StockResult, stock.calculate_profit("2023-01-18"))

        # Verificamos que los valores son coherentes
        self.assertIsInstance(result["profit"], float)
        self.assertIsInstance(result["purchase_price"], float)
        self.assertIsInstance(result["end_price"], float)
        self.assertEqual(result["profit"], result["end_price"] - result["purchase_price"])


if __name__ == "__main__":
    unittest.main()
