"""Aplicación Streamlit para mostrar el portfolio de stocks."""

from datetime import date, datetime, timedelta
from typing import cast

import streamlit as st

from classes.portfolio import Portfolio
from utils.formatting import format_currency, format_percentage

# Inicializar el portfolio en el estado de la sesión
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio()

st.set_page_config(
    page_title="Stock Portfolio Analyzer",
    page_icon="📈",
)

st.title("📈 Stock Portfolio Analyzer")
st.markdown(
    """
Esta aplicación permite analizar un portfolio de acciones.
Ingresa los símbolos y fechas para calcular los rendimientos.
"""
)

# Crear las columnas principales para la interfaz
left_col, right_col = st.columns([1, 1])

# Columna izquierda para agregar stocks
with left_col:
    st.subheader("Agregar Acciones")

    # Checkbox fuera del formulario para que sea reactivo
    use_manual = st.checkbox("Ingresar símbolo manualmente")

    with st.form("add_stock"):
        if use_manual:
            symbol = st.text_input(
                "Símbolo de la acción",
                help="Ejemplo: MELI para MercadoLibre, GLOB para Globant, etc.",
            ).upper()
        else:
            # Lista de símbolos populares con sus nombres
            stock_options = {
                "AAPL": "Apple Inc.",
                "MSFT": "Microsoft Corporation",
                "GOOGL": "Alphabet Inc.",
                "AMZN": "Amazon.com Inc.",
                "META": "Meta Platforms Inc.",
                "TSLA": "Tesla Inc.",
                "NVDA": "NVIDIA Corporation",
                "JPM": "JPMorgan Chase & Co.",
                "V": "Visa Inc.",
                "WMT": "Walmart Inc.",
                "KO": "Coca-Cola Company",
                "DIS": "Walt Disney Company",
                "NFLX": "Netflix Inc.",
                "MELI": "MercadoLibre Inc.",
                "GLOB": "Globant SA",
            }

            symbol = st.selectbox(
                "Selecciona una acción",
                options=list(stock_options.keys()),
                format_func=lambda x: f"{x} - {stock_options[x]}",
            )

        purchase_date_input = st.date_input(
            "Fecha de compra",
            value=cast(date, datetime.now().date() - timedelta(days=30 * 3)),
            max_value=datetime.now().date(),
        )

        if st.form_submit_button("Agregar Acción"):
            try:
                if isinstance(purchase_date_input, date):
                    st.session_state.portfolio.add_stock(
                        symbol, purchase_date_input.strftime("%Y-%m-%d")
                    )
                    st.success(f"✅ Acción {symbol} agregada exitosamente")
                else:
                    st.error("❌ Fecha de compra inválida")
            except ValueError as e:
                st.error(f"❌ Error: {str(e)}")

# Columna derecha para mostrar el portfolio
with right_col:
    st.subheader("Acciones en el Portfolio")

    if st.session_state.portfolio.stocks:
        stock_data = []
        for stock in st.session_state.portfolio.stocks:
            stock_data.append(
                {
                    "Símbolo": stock.symbol,
                    "Fecha de Compra": stock.purchase_date.strftime("%Y-%m-%d"),
                    "Precio de Compra": format_currency(stock.purchase_price),
                }
            )

        st.table(stock_data)
    else:
        st.info(
            "Las acciones de tu portfolio aparecerán aquí una vez que agregues al menos una acción"
        )

# Después de agregar stocks y antes de la sección de análisis
if st.session_state.portfolio.stocks:
    st.subheader("Análisis del Portfolio")

    # Crear dos columnas para las fechas
    col1, col2 = st.columns(2)

    with col1:
        start_date_input = st.date_input(
            "Fecha inicial de análisis",
            value=cast(date, datetime.now().date() - timedelta(days=30 * 6)),
            max_value=datetime.now().date(),
        )

    with col2:
        end_date_input = st.date_input(
            "Fecha final de análisis",
            value=datetime.now().date(),
            max_value=datetime.now().date(),
        )

    if st.button("Calcular Rendimiento"):
        try:
            # Validar que tenemos fechas válidas
            if not isinstance(start_date_input, date) or not isinstance(end_date_input, date):
                st.error("❌ Fechas de análisis inválidas")
            elif end_date_input <= start_date_input:
                st.error("❌ La fecha final debe ser posterior a la fecha inicial")
            else:
                results = st.session_state.portfolio.profit(
                    start_date=start_date_input.strftime("%Y-%m-%d"),
                    end_date=end_date_input.strftime("%Y-%m-%d"),
                )

                # Mostrar métricas principales
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Inversión Total", format_currency(results["total_investment"]))
                with col2:
                    st.metric("Beneficio Total", format_currency(results["total_profit"]))
                with col3:
                    st.metric(
                        "Retorno Anualizado", format_percentage(results["annualized_return"] * 100)
                    )

                # Mostrar detalles por acción
                st.subheader("Detalles por Acción")
                for stock in results["stocks"]:
                    profit_percentage = (stock["profit"] / stock["purchase_price"]) * 100
                    expander_title = (
                        f"{stock['symbol']} - "
                        f"Comprado: {stock['purchase_date'].strftime('%Y-%m-%d')} - "
                        f"Beneficio: {format_currency(stock['profit'])} - "
                        f"Rendimiento: {format_percentage(profit_percentage)}"
                    )
                    with st.expander(expander_title):
                        st.write(f"Fecha de compra: {stock['purchase_date'].strftime('%Y-%m-%d')}")
                        st.write(f"Precio de compra: {format_currency(stock['purchase_price'])}")
                        st.write(f"Precio actual: {format_currency(stock['end_price'])}")
                        st.write(f"Beneficio: {format_currency(stock['profit'])}")
                        st.write(f"Rendimiento: {format_percentage(profit_percentage)}")

        except ValueError as e:
            st.error(f"❌ Error: {str(e)}")

    # Agregar botón para reiniciar el portfolio
    if st.button("Reiniciar Portfolio"):
        st.session_state.portfolio = Portfolio()
        st.rerun()

else:
    st.info("👆 Agrega algunas acciones para comenzar el análisis")
