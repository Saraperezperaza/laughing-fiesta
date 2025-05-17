import sqlite3

def conectar():
    return sqlite3.connect('base_de_datos.db')
