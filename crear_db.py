import sqlite3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

crear_tabla = """CREATE TABLE IF NOT EXISTS envios (
                    id INTEGER PRIMARY KEY,
                    receiver text,
                    subject text,
                    filename text,
                    file_location text,
                    sql_location text,
                    periodicidad text,
                    hora_ejecucion text,
                    dia_semana int,
                    dia_ejecucion int,
                    generado int DEFAULT 0,
                    enviado int DEFAULT 0
                    )"""

cursor.execute(crear_tabla)
conn.commit()
conn.close()