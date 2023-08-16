import logging, os, manejador_db
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
import multiprocessing as mp

os.chdir(os.path.dirname(os.path.abspath(__file__)))

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_weekday = now.weekday()
current_day = now.day

conn_string = 'oracle+cx_oracle://CONSULTA_BI:ZaBgt5q12wsx@rodb.gdeba.gba.gob.ar:10521/?service_name=dpmamjgm.gdeba.gba.gob.ar'
engine = create_engine(conn_string)

logging.basicConfig(
    filename='archivo.log', 
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%m-%y %H:%M:%S',
    level=logging.INFO
    )

def generar_reporte(generacion):
    #try:
        with engine.connect() as conn:
            query = open(generacion['sql_location'], 'r').read()
            data = pd.read_sql(text(query), con=conn)
            data.to_excel(generacion.file_location, index=False)
            name = str(generacion.file_location).split("/")[-1]
            logging.info(f"{name} <- generado.")

if __name__ == '__main__':
    g = {'sql_location': './GENERALES/test.sql'}
    generar_reporte(g)