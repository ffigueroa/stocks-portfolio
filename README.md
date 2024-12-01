# Portfolio de Stocks

[![Tests](https://github.com/ffigueroa/stocks-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/ffigueroa/stocks-portfolio/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

Portfolio de Stocks que permite agregar acciones con fecha de compra, calcular beneficios y retorno anualizado del portfolio en un rango de fechas.

[Changelog](CHANGELOG.md)

## Características

- Manejo de múltiples acciones en un portfolio
- Cálculo de beneficios y retorno anualizado
- Ajuste automático para días inhábiles
- Manejo robusto de errores
- Validación de símbolos y fechas
- Tipos estáticos para mayor seguridad
- Tests unitarios automatizados

## Estructura del Proyecto

```
stocks/
├── classes/          # Clases principales
│   ├── __init__.py
│   ├── stock.py      # Manejo de acciones individuales
│   └── portfolio.py  # Gestión del portfolio
├── models/          # Definiciones de tipos/modelos
│   ├── __init__.py
│   ├── stock.py      # Tipos para acciones
│   └── portfolio.py  # Tipos para portfolio
├── utils/           # Utilidades
│   ├── __init__.py
│   ├── market.py     # Funciones de mercado
│   └── formatting.py # Funciones de formateo
├── tests/           # Tests unitarios
│   ├── __init__.py
│   ├── test_stock.py
│   └── test_portfolio.py
├── example.py        # Ejemplo de uso
├── pyproject.toml    # Configuración del proyecto y dependencias
├── CHANGELOG.md      # Registro de cambios
├── LICENSE          # Licencia MIT
├── .pre-commit-config.yaml  # Configuración de pre-commit
├── .cz.toml         # Configuración de commitizen
├── .flake8          # Configuración de flake8
├── .gitignore       # Archivos ignorados por git
└── README.md        # Documentación
```

## Requisitos

- Python 3.10+
- pip (para instalar dependencias)
- git (para control de versiones)

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/ffigueroa/stocks-portfolio.git
cd stocks-portfolio

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install .            # Instala el proyecto y sus dependencias

# Configurar git hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

## Uso Rápido

```python
from classes.portfolio import Portfolio

# Crear portfolio y agregar acciones
portfolio = Portfolio()
portfolio.add_stock("AAPL", "2023-01-14")  # Se ajustará al siguiente día hábil si es necesario
portfolio.add_stock("MSFT", "2023-06-01")

# Calcular beneficios
result = portfolio.profit("2023-01-01", "2024-10-25")
print(f"Beneficio total: ${result['total_profit']:,.2f}")
print(f"Retorno anualizado: {result['annualized_return']*100:.2f}%")
```

También puedes probar el ejemplo incluido que muestra todas las funcionalidades:

```bash
# Ejecutar ejemplo con 3 stocks (AAPL, MSFT, GOOGL)
python example.py

# Salida esperada:
Portfolio creado

Intentando agregar AAPL con fecha 2023-01-14
Nota: La compra de AAPL se ejecutará el 2023-01-17 (siguiente día hábil después de 2023-01-14)

Intentando agregar MSFT con fecha 2023-06-01

Intentando agregar GOOGL con fecha 2023-09-17
Nota: La compra de GOOGL se ejecutará el 2023-09-18 (siguiente día hábil después de 2023-09-17)

Stocks del portfolio al 2024-10-25:
AAPL:
  Fecha de compra: 2023-01-17
  Precio de compra: $135.94
  Precio actual: $170.77
  Beneficio: $34.83
  Rendimiento: 25.62%
...

Resumen del Portfolio:
Inversión total: $408.23
Valor actual: $514.67
Beneficio total: $106.44
Retorno anualizado: 15.23%
```

## Desarrollo

### Comandos Comunes

```bash
# Tests
pytest                # Ejecutar todos los tests
pytest tests/ -v      # Ejecutar tests con más detalle
pytest -k "test_portfolio" # Ejecutar un test específico

# Formateo y verificación de código
black .              # Formatear código
isort .              # Ordenar imports
flake8 .             # Verificar estilo
mypy .               # Verificar tipos

```

### Flujo de Trabajo

1. Crear rama para nueva característica
```bash
git checkout -b feat/nombre-feature
```

2. Realizar cambios siguiendo las guías de estilo
   - El código se formatea automáticamente con black/isort
   - Los hooks de pre-commit verifican:
     - Formato de código (black)
     - Orden de imports (isort)
     - Estilo de código (flake8)
     - Tipos estáticos (mypy)
     - Tests unitarios (pytest)
     - Formato de commit (commitizen)

3. Hacer commit de los cambios
```bash
git add .
git commit -m "feat: descripción del cambio"  # Usar Conventional Commits
```

## Características Técnicas

- Arquitectura modular y bien organizada:
  - `classes/`: Implementaciones principales
  - `models/`: Definiciones de tipos
  - `utils/`: Utilidades separadas por responsabilidad
- Tipos estáticos con mypy para mayor seguridad
- Documentación completa con docstrings
- Manejo de errores con excepciones específicas
- Logging configurable para debugging
- Tests unitarios con pytest
- Commits convencionales con Commitizen
- Pre-commit hooks para calidad de código
- Configuración centralizada en pyproject.toml
- CI/CD con GitHub Actions

## Limitaciones

- Solo soporta acciones disponibles en Yahoo Finance
- No maneja divisas diferentes a USD
- No incluye dividendos en los cálculos
- No soporta operaciones en corto

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
