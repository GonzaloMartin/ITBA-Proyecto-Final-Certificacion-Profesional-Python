# Certificación Profesional en Python: Proyecto Final.

## Autor
 - Gonzalo Montalvo | [@GonzaloMartin](https://github.com/GonzaloMartin).

## Contenido

 1. [Documentación](#documentación)
 2. [Resumen](#resumen)
 3. [Detalles de Implementación](#detalles-de-implementación)
    - [Menú principal](#menú-principal)
    - [Actualización de datos](#actualización-de-datos)
    - [Visualización de datos](#visualización-de-datos)
    - [Resumen](#resumen)
    - [Gráfico](#gráfico)
 4. [Extras](#extras)
 5. [Links útiles](#links-útiles)

## Documentación
    
La documentación funcional y técnica del sistema se encuentra en el siguiente link:
 - [Documentación](docs/documentacion.md)

## Resumen

Se implementa un programa que permita leer datos de una API de finanzas, guardarlos en una base de datos y graficarlos.
La API elegida es [Polygon.io](https://polygon.io/docs/stocks/getting-started) y la base de datos elegida es SQLite.

## Detalles de Implementación

### Menú principal

El programa presenta un menú principal donde puedan elegirse las siguientes dos opciones:

 1. Actualización de datos
 2. Visualización de datos
 3. Salir

### Actualización de datos

El programa solicita al usuario el valor de un ticker, una fecha de inicio y una fecha de fin.
Estos valores los pide a la API y guarda los datos en la base de datos.

Ejemplo:
```
>>> Ingrese ticker a pedir:
AAPL
>>> Ingrese fecha de inicio:
2022-01-01
>>> Ingrese fecha de fin:
2022-07-01
>>> Pidiendo datos ...
>>> Datos guardados correctamente
```

### Visualización de datos

El sistema permite dos visualizaciones de datos:

 1. Resumen
 2. Gráfico de ticker

### Resumen

Muestra un resumen de los datos guardados en la base de datos.

Ejemplos:
```
>>> Los tickers guardados en la base de datos son:
>>> AAPL - 2022/01/01 <-> 2022/07/01
>>> AAL  - 2021/01/01 <-> 2022/07/01
```

### Gráfico

El sistema permite graficar los datos guardados para un ticker específico.

Ejemplo:
```
>>> Ingrese el ticker a graficar:
AAL
```
El estilo de gráfico elegido es el gráfico de velas (candle graph).

## Extras

Extras agregados al proyecto:

 - Actualización de rangos en base de datos considerando lo guardado. Ej: Si tengo del 2022/01/01 al 2022/07/01 y pido del 2021/01/01 al 2022/07/01 únicamente debo pedir del 2021/01/01 al 2021/12/31.
 - Manejo de errores de red y reconexiones.
 - Visualización de parámetros técnicos.

## Links útiles

 1. [API de valores de finanzas] (https://polygon.io/docs/stocks/getting-started).
 2. [Libreria de base de datos] (https://docs.python.org/3/library/sqlite3.html).
