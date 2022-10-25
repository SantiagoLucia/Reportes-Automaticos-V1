import logging, os, manejador_db
from datetime import datetime
import pandas as pd
import sqlalchemy
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from config import CON_URL

def oracle_loggin():
    engine = sqlalchemy.create_engine(CON_URL)
    conn = engine.connect()
    return conn


logging.basicConfig(
    filename='archivo.log', 
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%m-%y %H:%M:%S',
    level=logging.INFO
    )

generaciones = manejador_db.generaciones_pendientes()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_weekday = now.weekday()
current_day = now.day

for generacion in generaciones:
    id = generacion[0]
    file_location = generacion[1]
    sql_location = generacion[2]
    periodicidad = generacion[3]
    hora_ejecucion = generacion[4]
    dia_semana = generacion[5]
    dia_ejecucion = generacion[6]

    if periodicidad == "DIARIO":
        if datetime.strptime(hora_ejecucion,"%H:%M:%S") > datetime.strptime(current_time,"%H:%M:%S"):
            continue

    if periodicidad == "SEMANAL":
        if current_weekday == dia_semana:
            if datetime.strptime(hora_ejecucion,"%H:%M:%S") > datetime.strptime(current_time,"%H:%M:%S"):
                continue 
        else:
            manejador_db.modificar(id, 'generado')
            manejador_db.modificar(id, 'enviado')
            continue

    if periodicidad == "MENSUAL":
        if current_day == dia_ejecucion:
            if datetime.strptime(hora_ejecucion,"%H:%M:%S") > datetime.strptime(current_time,"%H:%M:%S"):
                continue 
        else:
            manejador_db.modificar(id, 'generado')
            manejador_db.modificar(id, 'enviado')
            continue 

    if os.path.exists(file_location):
        os.remove(file_location)

    query = ""
    with open(sql_location, "r", encoding="utf8") as file:
        for _ in file.readlines():
            query += _

    intentos = 0
    while intentos < 3:
        try:
            conexion = oracle_loggin()    
        except:
            intentos += 1
            logging.error(f"Exception occurred - TNS connection time out. ({3-intentos}) intentos restantes")        
        else:
            try:
                data = pd.read_sql(query, conexion)
                data.to_excel(file_location, index=False)
                manejador_db.modificar(id, 'generado')
                logging.info(f"{file_location} <- generado.")
                break
            except:
                logging.error(f"Exception occurred - Error en {sql_location}")
                break