import requests
import sqlite3
from conftest import *
from datetime import datetime
from cryptography.fernet import Fernet

def crear_base():
    # Crear la base de datos si no existe

    con = sqlite3.connect('finanzas.db')
    return con

def crear_stock_market(con):
    # Crea una tabla con los tickers existentes en la base de datos

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
    # Crear una tabla para un ticker si no existe

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
    # Consulta si un ticker ya existe en la base de datos
    valor = False
    cursorObj = con.cursor()
    query = f"""
        SELECT ticker FROM STOCK_MARKET WHERE ticker = '{ticker}'
        """
    cursorObj.execute(query)
    rows = cursorObj.fetchall()
    if len(rows) > 0: valor = True
    return valor

def insertar_datos_stock_market(con, ticker, fch_ini, fch_fin):
    # Insertar datos en la base de datos

    cursorObj = con.cursor()
    data = (ticker, fch_ini, fch_fin)
    query = f"""
    INSERT INTO STOCK_MARKET (ticker, fecha_ini, fecha_fin)
    VALUES (?, ?, ?)
    """
    cursorObj.execute(query, data)
    con.commit()

def actualizar_stock_market(con, ticker, fch_ini, fch_fin):
    # Actualizar datos en la base de datos

    cursorObj = con.cursor()
    data = (fch_ini, fch_fin, ticker)
    query = f"""
    UPDATE STOCK_MARKET SET fecha_ini = ?, fecha_fin = ? WHERE ticker = ?
    """
    cursorObj.execute(query, data)
    con.commit()

def insertar_datos_ticker(con, ticker, fecha, precio_inicio, precio_cierre, precio_min, precio_max, precio_media, volumen, num_trx):
    # Insertar datos en la base de datos

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
        # y establecer rangos de fecha sin repetirlas.  Se establece  una feca como UNIQUE
        # e inserto sólamente los registros que no existan en la base de datos
        # para no generar sobrepoblamiento.

        if "UNIQUE constraint failed" in str(e):
            pass  # Omito insertar los registros de fechas que ya existen en la BD.
        else:
            print(f"Error: {e}")

def consultar_sql(con, query):
    # Consultar datos en la base de datos

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
    # Función para obtener el año actual

    now = datetime.now()
    return now.year

def get_fecha():
    # Función para obtener la fecha actual en formato YYYY-MM-DD

    now = datetime.now()
    return now.strftime("%Y-%m-%d")

def get_clv_descompuesta_a():
    return "Bearer "

def get_clv_descompuesta_p():
    return "QePQ4Fm3Q9pbHW0kgd"

def get_clv_descompuesta_k():
    return "9E9ra5033_P4_N"

def convertir_fecha_api(timestamp_milisegs):
    # Función para convertir timestamp de milisegundos a formato YYYY-MM-DD

    timestamp_segs = timestamp_milisegs / 1000.0
    fecha = datetime.fromtimestamp(timestamp_segs)
    return fecha.strftime("%Y-%m-%d")

def get_au():
    cc = generar_clv()
    return descifrar_api_k(apk_cifrada=cc[0], clave_cifrado=cc[1])

def get_verificar_servicio():
    # Función para verificar el servicio de la API

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
    return Fernet.generate_key()

def cifrar_api_k(api_k, clave_cifrado):
    cipher_suite = Fernet(clave_cifrado)
    api_k_cifrada = cipher_suite.encrypt(api_k.encode())
    return api_k_cifrada

def generar_clv():
    clave_cifrado = generar_clv_cifrado()
    apk = get_clv_descompuesta_a() + get_clv_descompuesta_p() + get_clv_descompuesta_k()
    apk_cifrada = cifrar_api_k(apk, clave_cifrado)
    return apk_cifrada, clave_cifrado

def descifrar_api_k(apk_cifrada, clave_cifrado):
    cipher_suite = Fernet(clave_cifrado)
    api_de_k = cipher_suite.decrypt(apk_cifrada).decode()
    return api_de_k
