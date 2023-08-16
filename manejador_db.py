from sqlalchemy import create_engine, text
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def envios_pendientes():
    engine = create_engine(rf"sqlite:///data.db")
    with engine.connect() as conn:
        resultado = conn.execute(text("""SELECT id, receiver, subject, filename, file_location, 
        periodicidad, hora_ejecucion, dia_semana, dia_ejecucion, receiver_cc, receiver_cco 
        FROM envios WHERE enviado = 0 and generado = 1"""))
        return resultado.mappings().all()

def generaciones_pendientes():
    engine = create_engine(rf"sqlite:///data.db")
    with engine.connect() as conn:
        resultado = conn.execute(text("""SELECT id, file_location, sql_location, periodicidad, 
                    hora_ejecucion, dia_semana, dia_ejecucion FROM envios WHERE generado = 0"""))
        return resultado.mappings().all()    

def restantes(col):
    engine = create_engine(rf"sqlite:///data.db")
    with engine.connect() as conn:
        resultado = conn.execute(text(f"SELECT count(*) AS cantidad FROM envios WHERE {col} = 0"))
        return resultado.mappings().first()  

def inicializar():
    engine = create_engine(rf"sqlite:///data.db")
    with engine.connect() as conn:
        conn.execute(text("UPDATE envios SET enviado = 0, generado = 0"))  

def modificar(id, col):
    engine = create_engine(rf"sqlite:///data.db")
    with engine.connect() as conn:
        conn.execute(
            text(f"UPDATE envios SET {col} = 1 WHERE id = :id"),
            {'id': id}
            )