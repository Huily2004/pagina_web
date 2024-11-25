import mysql.connector


def obtener_conexion():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="proyecto_final",
    )