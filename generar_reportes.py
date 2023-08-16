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

conn_string = ""
engine = create_engine(conn_string)

logging.basicConfig(
    filename="archivo.log",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
    level=logging.INFO,
)


def generar_reporte(generacion):
    try:
        with engine.connect() as conn:
            query = open(generacion.sql_location, "r").read()
            data = pd.read_sql(text(query), con=conn)
            data.to_excel(generacion.file_location, index=False)
            name = str(generacion.file_location).split("/")[-1]
            manejador_db.modificar(generacion.id, "generado")
            logging.info(f"{name} <- generado.")
    except:
        logging.error(f"Exception occurred - Error en {generacion.file_location}")


def para_ejecutar(generacion):
    if generacion.periodicidad == "DIARIO":
        if datetime.strptime(generacion.hora_ejecucion, "%H:%M:%S") > datetime.strptime(
            current_time, "%H:%M:%S"
        ):
            return False

    if generacion.periodicidad == "SEMANAL":
        if current_weekday == generacion.dia_semana:
            if datetime.strptime(
                generacion.hora_ejecucion, "%H:%M:%S"
            ) > datetime.strptime(current_time, "%H:%M:%S"):
                return False
        else:
            manejador_db.modificar(generacion.id, "generado")
            manejador_db.modificar(generacion.id, "enviado")
            return False

    if generacion.periodicidad == "MENSUAL":
        if current_day == generacion.dia_ejecucion:
            if datetime.strptime(
                generacion.hora_ejecucion, "%H:%M:%S"
            ) > datetime.strptime(current_time, "%H:%M:%S"):
                return False
        else:
            manejador_db.modificar(generacion.id, "generado")
            manejador_db.modificar(generacion.id, "enviado")
            return False

    return True


if __name__ == "__main__":
    lista_procesos = []

    with mp.Pool() as pool:
        for generacion in manejador_db.generaciones_pendientes():
            if not para_ejecutar(generacion):
                continue

            if os.path.exists(generacion.file_location):
                os.remove(generacion.file_location)

            proc = pool.apply_async(generar_reporte, args=(generacion,))
            lista_procesos.append(proc)

        for proceso in lista_procesos:
            proceso.wait()
