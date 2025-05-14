import mysql.connector
from mysql.connector import Error
config = {
    'host': 'prog2.myslq.pythonanywhere-services.com',
    'user': 'prog2',
    'password': 'test_password',
    'database': 'prog2$default',
}

def conectar_a_bdd():
    try:
        conexion = mysql.connector.connect(**config)
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None