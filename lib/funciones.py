import requests
import sqlite3
from conftest import *
from datetime import datetime
from cryptography.fernet import Fernet

def crear_base():
    """
    Crea la base de datos si no existe.

    :return: con (objeto conexión)
    """

    con = sqlite3.connect('finanzas.db')
    return con

def crear_stock_market(con):
    """
    Crea la tabla STOCK_MARKET si no existe.
    Esta tabla almacena los tickers existentes en la base de datos.

    :param con: Objeto conexión.
    :return: None
    """

    cursorObj = con.cursor()
    query = f"""
        CREATE TABLE IF NOT EXISTS STOCK_MARKET (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE,
            fecha_ini TEXT,
            fecha_fin TEXT
        )
        """
    cursorObj.execute(query)
    con.commit()

def crear_tabla_ticker(con, ticker):
    """
    Crea una tabla para un ticker si no existe.
    Esta tabla almacena los datos de un ticker.

    :param con: Objeto conexión.
    :param ticker: Ticker del cual se almacenarán los datos.
    :return: None
    """

    cursorObj = con.cursor()
    query = f"""
    CREATE TABLE IF NOT EXISTS {ticker} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT UNIQUE,
        precio_inicio REAL,
        precio_cierre REAL,
        precio_min REAL,
        precio_max REAL,
        precio_media REAL,
        volumen REAL,
        num_trx INTEGER
    )
    """
    cursorObj.execute(query)
    con.commit()

def consultar_stock_market(con, ticker):
    """
    Consulta si un ticker ya existe en la base de datos.
    La tabla STOCK_MARKET almacena los tickers existentes.

    :param con: Objeto conexión.
    :param ticker: Ticker a consultar.
    :return: valor (bool) True si el ticker existe, False si no existe.
    """

    valor = False
    cursorObj = con.cursor()
    query = f"""
        SELECT ticker FROM STOCK_MARKET WHERE ticker = '{ticker}'
        """
    cursorObj.execute(query)
    rows = cursorObj.fetchall()
    if len(rows) > 0:
        valor = True
    return valor

def insertar_datos_stock_market(con, ticker, fch_ini, fch_fin):
    """
    Inserta datos en la tabla STOCK_MARKET.
    Esta tabla almacena los tickers existentes en la base de datos.

    :param con: Objeto conexión.
    :param ticker: Ticker a insertar.
    :param fch_ini: Fecha de inicio de los datos.
    :param fch_fin: Fecha de fin de los datos.
    :return: None
    """

    cursorObj = con.cursor()
    data = (ticker, fch_ini, fch_fin)
    query = f"""
    INSERT INTO STOCK_MARKET (ticker, fecha_ini, fecha_fin)
    VALUES (?, ?, ?)
    """
    cursorObj.execute(query, data)
    con.commit()

def actualizar_stock_market(con, ticker, fch_ini, fch_fin):
    """
    Actualiza datos en la tabla STOCK_MARKET.
    Esta tabla almacena los tickers existentes en la base de datos.
    Los actualiza si ya existen.

    :param con: Objeto conexión.
    :param ticker: Ticker a actualizar.
    :param fch_ini: Fecha de inicio de los datos.
    :param fch_fin: Fecha de fin de los datos.
    :return: None
    """

    cursorObj = con.cursor()
    data = (fch_ini, fch_fin, ticker)
    query = f"""
    UPDATE STOCK_MARKET SET fecha_ini = ?, fecha_fin = ? WHERE ticker = ?
    """
    cursorObj.execute(query, data)
    con.commit()

def insertar_datos_ticker(con, ticker, fecha, precio_inicio, precio_cierre, precio_min, precio_max, precio_media, volumen, num_trx):
    """
    Inserta datos en la tabla de un ticker.
    Esta tabla almacena los datos de un ticker.

    :param con: Objeto conexión.
    :param ticker: Ticker a insertar.
    :param fecha: Fecha del registro.
    :param precio_inicio: Precio de apertura.
    :param precio_cierre: Precio de cierre.
    :param precio_min: Precio mínimo.
    :param precio_max: Precio máximo.
    :param precio_media: Precio medio.
    :param volumen: Volumen.
    :param num_trx: Número de transacciones.
    :return: None
    """

    cursorObj = con.cursor()
    data = (fecha, precio_inicio, precio_cierre, precio_min, precio_max, precio_media, volumen, num_trx)
    query = f"""
    INSERT INTO {ticker} (fecha, precio_inicio, precio_cierre, precio_min, precio_max, precio_media, volumen, num_trx)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    try:
        cursorObj.execute(query, data)
        con.commit()
    except sqlite3.IntegrityError as e:
        # Este control ya contempla el EXTRA que piden sobre no duplicar fechas
        # y establecer rangos de fecha sin repetirlas.  Se establece  una fecha como UNIQUE
        # e inserto sólamente los registros que no existan en la base de datos
        # para no generar sobrepoblamiento.

        if "UNIQUE constraint failed" in str(e):
            pass  # Omito insertar los registros de fechas que ya existen en la BD.
        else:
            print(f"Error: {e}")

def consultar_sql(con, query):
    """
    Consulta datos en la base de datos. Los datos se obtienen según la query.

    :param con: Objeto conexión.
    :param query: Consulta a realizar.
    :return: rows (list) Lista con los datos obtenidos.
    """

    rows = None
    cursorObj = con.cursor()
    try:
        cursorObj.execute(query)
        rows = cursorObj.fetchall()
    except sqlite3.IntegrityError as e:
        if "no such table" in str(e):
            print("El ticker no existe en la base de datos.")
        else:
            print("Error:", e)
    return rows

def get_anio():
    """
    Función para obtener el año actual.

    :return: now.year (int) Año actual.
    """

    now = datetime.now()
    return now.year

def get_fecha():
    """
    Función para obtener la fecha actual en formato YYYY-MM-DD.

    :return: now.strftime("%Y-%m-%d") (str) Fecha actual en formato YYYY-MM-DD.
    """

    now = datetime.now()
    return now.strftime("%Y-%m-%d")

def get_clv_descompuesta_a():
    """
    Función genérica.

    :return: Un resultado.
    """
    return "Bearer "

def get_clv_descompuesta_p():
    """
    Función genérica.

    :return: Un resultado.
    """

    return "QePQ4Fm3Q9pbHW0kgd"

def get_clv_descompuesta_k():
    """
    Función genérica.

    :return: Un resultado.
    """

    return "9E9ra5033_P4_N"

def convertir_fecha_api(timestamp_milisegs):
    """
    Función para convertir timestamp de milisegundos a formato YYYY-MM-DD
    El estilo de fecha es el que se utiliza en la API. Esta es expresada en UNIX Time.
    Se divide el timestamp en milisegundos entre 1000 para obtener el timestamp en segundos.

    :param timestamp_milisegs: Timestamp en milisegundos.
    :return: fecha.strftime("%Y-%m-%d") (str) Fecha en formato YYYY-MM-DD.
    """

    timestamp_segs = timestamp_milisegs / 1000.0
    fecha = datetime.fromtimestamp(timestamp_segs)
    return fecha.strftime("%Y-%m-%d")

def get_au():
    """
    Función genérica.

    :return: Un resultado.
    """

    cc = generar_clv()
    return descifrar_api_k(apk_cifrada=cc[0], clave_cifrado=cc[1])

def get_verificar_servicio():
    """
    Función para verificar el servicio de la API. La misma retorna un JSON con el estado del servicio.
    Criterio de Aceptación: El servicio de la API debe estar disponible.

    :return: response: Respuesta de la API. response_json: Respuesta de la API en formato JSON. (Una Tupla)
    """

    url = "https://api.polygon.io/v1/marketstatus/now"
    au = get_au()

    headers = {
        'Authorization': au
    }

    ignorarWarnings()
    response = requests.get(url, headers=headers, verify=False)
    response_json = response.json()
    return response, response_json

def get_datos_polygon(ticker, fecha_inicio, fecha_fin):
    # Función para obtener datos de la API según ticker y fechas
    """
    Función para obtener datos de la API según ticker y fechas.
    Criterio de Aceptación: Se debe obtener los datos de la API.

    :param ticker: Ticker del cual se obtendrán los datos.
    :param fecha_inicio: Fecha de inicio de los datos.
    :param fecha_fin: Fecha de fin de los datos.
    :return: response: Respuesta de la API. response_json: Respuesta de la API en formato JSON. (Una Tupla)
    """

    url_base = "https://api.polygon.io/v2/aggs/ticker/"
    url_endp = "/range/1/day/"
    url = url_base + ticker + url_endp + fecha_inicio + "/" + fecha_fin
    au = get_au()

    headers = {
        'Authorization': au
    }

    ignorarWarnings()
    response = requests.get(url, headers=headers, verify=False)
    response_json = response.json()
    return response, response_json

def generar_clv_cifrado():
    """
    Función genérica.

    :return: Un resultado.
    """
    return Fernet.generate_key()

def cifrar_api_k(api_k, clave_cifrado):
    """
    Función genérica.

    :return: Un resultado.
    """

    cipher_suite = Fernet(clave_cifrado)
    api_k_cifrada = cipher_suite.encrypt(api_k.encode())
    return api_k_cifrada

def generar_clv():
    """
    Función genérica.

    :return: Un resultado.
    """

    clave_cifrado = generar_clv_cifrado()
    apk = get_clv_descompuesta_a() + get_clv_descompuesta_p() + get_clv_descompuesta_k()
    apk_cifrada = cifrar_api_k(apk, clave_cifrado)
    return apk_cifrada, clave_cifrado

def descifrar_api_k(apk_cifrada, clave_cifrado):
    """
    Función genérica.

    :return: Un resultado.
    """

    cipher_suite = Fernet(clave_cifrado)
    api_de_k = cipher_suite.decrypt(apk_cifrada).decode()
    return api_de_k
