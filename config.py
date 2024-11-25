import os


class Config:
    SECRET_KEY = os.urandom(24)  # Llave secreta para sesiones
    DEBUG = True  # Activa el modo debug para desarrollo


# Puedes agregar más configuraciones aquí