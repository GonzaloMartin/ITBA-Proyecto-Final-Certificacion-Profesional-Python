import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from lib.funciones import *


def actualizar_datos(ticker_rq, fecha_ini_rq, fecha_fin_rq):
    """
    Actualiza los datos de un ticker en la base de datos.
    Los datos se obtienen de la API de Polygon.io.

    :param ticker_rq: Ticker consultado.
    :param fecha_ini_rq: Fecha de inicio de la consulta.
    :param fecha_fin_rq: Fecha de fin de la consulta.
    :return: None
    """

    con = crear_base()  # Creo la conexión a la base de datos
    crear_stock_market(con)  # Crea la tabla de stock market si no existe

    # Obtener datos de la API
    response = get_datos_polygon(ticker=ticker_rq, fecha_inicio=fecha_ini_rq, fecha_fin=fecha_fin_rq)
    if response[0].status_code != 200:
        print("Error al obtener datos de la API. Status code: " + str(response[0].status_code))
        return

    if response[1]["resultsCount"] == 0:
        print("    > Ticker '" + ticker_rq + "' inexistente o no operable.")
        return

    # Verificar si el ticker ya existe en la base de datos
    existe_ticker = consultar_stock_market(con, ticker_rq)
    if not existe_ticker:
        crear_tabla_ticker(con, ticker_rq)

    # Preparo los datos para insertar en la BD
    datos = []
    for i in response[1]["results"]:
        fecha = convertir_fecha_api(i["t"])  # Convierto la fecha a formato YYYY-MM-DD
        datos.append((fecha, i["o"], i["c"], i["l"], i["h"], i["vw"], i["v"], i["n"]))

    # Insertar datos en la base de datos
    for i in datos:
        insertar_datos_ticker(con, ticker_rq, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])

    registro = consultar_sql(con, f"SELECT * FROM {ticker_rq} WHERE fecha = '{fecha_fin_rq}'")
    if len(registro) > 0:
        # Verificar si el ticker ya existe en la tabla stock_market
        existe_ticker = consultar_stock_market(con, ticker_rq)
        if existe_ticker:
            # Actualizar las fechas de inicio y fin del ticker
            fechas = consultar_sql(con, f"SELECT MIN(fecha), MAX(fecha) FROM {ticker_rq}")
            fecha_ini_stock = fechas[0][0]  # Obtengo la fecha de inicio, que es el primer elemento de la tupla
            fecha_fin_stock = fechas[0][1]  # Obtengo la fecha de fin, que es el segundo elemento de la tupla
            actualizar_stock_market(con, ticker_rq, fecha_ini_stock, fecha_fin_stock)
        else:
            # Insertar el ticker en la tabla stock_market
            insertar_datos_stock_market(con, ticker_rq, fecha_ini_rq, fecha_fin_rq)
        print("    > Datos guardados correctamente.")
    else:
        print("Error al guardar los datos.")

    con.close()

def mostrar_resumen():
    """
    Muestra un resumen de los tickers en la base de datos.
    La información mostrada es: ticker, fecha de inicio y fecha de fin.

    :return: None
    """

    con = crear_base()  # Creo la conexión a la base de datos
    print("\n        Resumen de datos:")
    print("\n        {:<10} {:<15} {:<15}".format("TICKER", "FECHA INICIO", "FECHA FIN"))
    print(" " * 8 + "-" * 38)

    datos = consultar_sql(con, 'SELECT ticker, fecha_ini, fecha_fin FROM STOCK_MARKET ORDER BY ticker')
    for registro in datos:
        print("        {:<10} {:<15} {:<15}".format(registro[0], registro[1], registro[2]))

    con.close()

def graficar_ticker(ticker):
    """
    Grafica el gráfico de velas para un ticker. El gráfico se muestra en una ventana emergente.
    El ticket que se graficará debe existir en la base de datos, tabla stock_market.
    No se graficará si el ticker no existe. Debe ser un ticker que haya sido consultado previamente.
    El gráfico se hace con la biblioteca mplfinance, que permite visualizar gráficos de velas.
    Esta biblioteca es una extensión de matplotlib.

    :param ticker: Ticker a graficar.
    :return: None
    """
    con = crear_base()  # Creo la conexión a la base de datos
    ticket_existe = consultar_stock_market(con, ticker=ticker)

    if not ticket_existe:
        print(f"        El ticker '{ticker}' no existe en la base de datos.")
        return

    query = f'''
    SELECT fecha, precio_inicio, precio_max, precio_min, precio_cierre, volumen
    FROM '{ticker}'
    ORDER BY fecha
    '''

    resultados = consultar_sql(con, query=query)
    if resultados is None:
        print(f"No hay datos para el ticker {ticker}.")
        return

    # Dataframe con la info
    df = pd.DataFrame(resultados, columns=['Fecha', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df.set_index('Fecha', inplace=True)

    # Graficar el gráfico de velas
    mpf.plot(df, type='candle', style='yahoo', title=f'Gráfico de Velas para {ticker}', ylabel='Precio',
             ylabel_lower='Volumen')

    con.close()

def get_parametros_tecnicos(ticker):
    """
    Muestra los parámetros técnicos de un ticker.
    Los parámetros técnicos son: fecha, precio de inicio, precio de cierre, precio mínimo, precio máximo,
    precio medio, volumen y número de transacciones. Se muestran en consola.
    El ticker debe existir en la base de datos, tabla stock_market.
    No se mostrará si el ticker no existe. Debe ser un ticker que haya sido consultado previamente.

    :param ticker: Ticker a consultar.
    :return: None
    """

    con = crear_base()  # Creo la conexión a la base de datos
    ticket_existe = consultar_stock_market(con, ticker=ticker)

    if not ticket_existe:
        print(f"        El ticker '{ticker}' no existe en la base de datos.")
        return

    query = f"""
            SELECT fecha, precio_inicio, precio_cierre, precio_min, precio_max, precio_media, volumen, num_trx 
            FROM '{ticker}' ORDER BY fecha
            """
    datos = consultar_sql(con, query=query)
    if len(datos) == 0:
        print("        El ticker no existe en la base de datos.")
        return

    print(f"\n        Resumen de Datos Técnicos para: '{ticker}'")
    print("\n        {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format("FECHA", "PRECIO INICIO",
                                                                                     "PRECIO CIERRE", "PRECIO MIN",
                                                                                     "PRECIO MAX", "MEDIA", "VOLUMEN",
                                                                                     "TRANSACCIONES"))
    print(" " * 8 + "-" * 127)

    for d in datos:
        print("        {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(d[0], d[1], d[2], d[3],
                                                                                       d[4], d[5], d[6], d[7]))

    con.close()

def iniciar_sistema():
    """
    Inicia el sistema de visualización de datos.
    Muestra un menú con las opciones disponibles. El usuario puede seleccionar una opción.
    Las opciones son: Actualización de datos, Visualización de datos y Salir.

    :return: None
    """

    while True:
        print("\nITBA - Certificacion Profesional en Python - PROYECTO FINAL")
        print(f"Autor: Gonzalo Martin Montalvo. (C) 2023 - {get_anio()}.")
        print("\nMenú Principal:")
        print("Polygon.io no permite visualizaciones del dia.")
        print("    1. Actualización de datos")
        print("    2. Visualización de datos")
        print("    3. Salir")
        opcion = input("\n    Seleccione una opción: ")

        if opcion == '1':
            ticker = input("    Ingrese ticker a consultar: ").upper()
            fecha_inicio = input("    Ingrese fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("    Ingrese fecha de fin (YYYY-MM-DD): ")
            print("    > Pidiendo datos ...")
            actualizar_datos(ticker, fecha_inicio, fecha_fin)
        elif opcion == '2':
            print("\n        Menú de Visualización:")
            print("        1. Resumen")
            print("        2. Gráfico de Ticker")
            print("        3. Parámetros Técnicos")
            subopcion = input("        Seleccione una opción del submenú: ")

            if subopcion == '1':
                mostrar_resumen()
            elif subopcion == '2':
                ticker = input("        Ingrese el ticker a Graficar: ").upper()
                graficar_ticker(ticker)
            elif subopcion == '3':
                ticker = input("        Ingrese el Ticker para ver sus detalles: ").upper()
                get_parametros_tecnicos(ticker)
            else:
                print("        Opción inválida.")
        elif opcion == '3':
            print("    Gracias por usar nuestro servicio. Bye!")
            break
        else:
            print("    Opción inválida.")
