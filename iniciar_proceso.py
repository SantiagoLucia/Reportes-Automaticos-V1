import os, time, manejador_db, logging

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    filename="archivo.log", 
    format="%(asctime)s - %(message)s", 
    datefmt="%d-%m-%y %H:%M:%S",
    level=logging.INFO
    )

logging.info("INICIO DE PROCESO.")

manejador_db.inicializar()

generando = True
enviando = True
generaciones_pendientes = manejador_db.restantes('generado')
envios_pendientes = manejador_db.restantes('enviado')

while generando or enviando:

    if generando:
        if generaciones_pendientes != 0:
            os.system('/usr/local/bin/python3.9 /srv/www/vhosts/autoreportes/generar_reportes.py')
        else:
            generando = False
            logging.info("Generacion de reportes finalizada.")

    if enviando:
        if envios_pendientes != 0:
            os.system('/usr/local/bin/python3.9 /srv/www/vhosts/autoreportes/mandar_mails.py')
        else:
            enviando = False
            logging.info("Envio de mails finalizado.")
    
    generaciones_pendientes = manejador_db.restantes('generado')
    envios_pendientes = manejador_db.restantes('enviado')
    
    if generaciones_pendientes == 0:
        generando = False

    if envios_pendientes == 0:
        enviando = False

    if generando or enviando:
        time.sleep(600)

logging.info("FIN DE PROCESO.")