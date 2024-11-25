import mysql.connector


def obtener_conexion():
    return mysql.connector.connect(
        host="blh32mgloalgepud7kjj-mysql.services.clever-cloud.com",
        user="uyot2szbhatqnnas",
        password="GnBU3C59U93SE7G5F844",
        database="blh32mgloalgepud7kjj",
    )