"""Utilidades de formato para mostrar datos."""

import logging

from models.portfolio import StockResult

logger = logging.getLogger(__name__)


def print_stock_info(stock: StockResult) -> None:
    """Print detailed stock information."""
    logger.info(f"\n{stock['symbol']}:")
    logger.info(f"  Fecha de compra: {stock['purchase_date']}")
    logger.info(f"  Precio de compra: {format_currency(stock['purchase_price'])}")
    logger.info(f"  Precio actual: {format_currency(stock['end_price'])}")
    logger.info(f"  Beneficio: {format_currency(stock['profit'])}")
    logger.info(f"  Rendimiento: {format_percentage(stock['profit']/stock['purchase_price']*100)}")
    logger.info(f"  Retorno anualizado: {format_percentage(stock['annualized_return']*100)}")


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """Format a number as percentage."""
    return f"{value:.2f}%"


def print_logo() -> None:
    """Print ASCII logo."""
    logo = """
          :::::::
       ::::::::::::       ::::::::::::::                                               :::
       :::::::::::::      :::       :::               :::                              :::
 :::::::::::::::::::      :::       :::: ::: :::::  :::::::: ::::    :::    :::::::::  :::
 :::::::::::::::::::      ::::::::  :::: :::::::::: :::::::: ::::    :::  :::::::::::: :::
 ::::::::::::::::::       ::::::::  :::: ::::   ::::  :::    ::::    :::  :::     :::: :::
 :::::::::::::::::        :::       :::: :::    ::::  :::    ::::    :::  :::     :::: :::
 ::::::::::               :::       :::: :::    ::::  ::::   :::::  ::::  ::::   ::::: :::
 ::::::::                 :::       :::: :::    ::::   :::::  ::::::::::   ::::::::::: :::
 :::::
    """
    print(logo)
