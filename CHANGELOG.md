# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2024-03-02

### Mejorado
- Mejorada la interacción del formulario en la interfaz Streamlit
- Simplificada la selección de símbolos con opción manual/predefinida
- Reorganizado el layout en dos columnas para mejor visualización
- Optimizada la presentación de métricas y detalles del portfolio

### Corregido
- Ajustada la persistencia del estado del portfolio en la sesión

## [1.1.0] - 2024-03-01

### Agregado
- Interfaz web con Streamlit para análisis interactivo del portfolio
- Persistencia del estado del portfolio en la interfaz Streamlit
- Capacidad de demo en vivo con despliegue en Streamlit Cloud
- Utilidades de mercado para manejo y validación de fechas
- Soporte para días no hábiles en cálculo de portfolio

### Cambiado
- Mejorado el cálculo de retorno anualizado usando promedio ponderado
- Refactorizadas las funciones de utilidad en módulos separados
- Mejorado el manejo de errores para datos de mercado
- Actualizada la documentación con uso de Streamlit

### Corregido
- Cálculo de retorno anualizado para períodos cortos
- Obtención de precios para días no hábiles en cálculo de portfolio


## [1.0.0] - 2024-02-29

### Agregado
- Implementación inicial de portfolio
- Clase Stock para manejo de acciones individuales
- Clase Portfolio para gestión de múltiples acciones
- Cálculo de beneficios y retorno anualizado
- Manejo de días inhábiles
- Tests unitarios
- Configuración de herramientas de desarrollo
- Documentación completa

### Características
- Obtención de datos desde Yahoo Finance
- Validación de símbolos y fechas
- Logging configurable
- Manejo de errores
- Tipos estáticos
