import sqlite3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def envios_pendientes():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT id, receiver, subject, filename, file_location, 
    periodicidad, hora_ejecucion, dia_semana, dia_ejecucion FROM envios WHERE enviado = 0""")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def generaciones_pendientes():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT id, file_location, sql_location, periodicidad, 
    hora_ejecucion, dia_semana, dia_ejecucion FROM envios WHERE generado = 0""")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def restantes(col):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM envios WHERE {col} = 0")
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

def inicializar():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE envios SET enviado = 0, generado = 0")
    conn.commit()
    conn.close()
    return

def modificar(id, col):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE envios SET {col} = 1 WHERE id = ?",(id,))
    conn.commit()
    conn.close()    
    return