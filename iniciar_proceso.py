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

while generando or enviando:

    if manejador_db.restantes('generado').cantidad > 0:
        os.system('/usr/local/bin/python3.9 /srv/www/vhosts/autoreportes_test/generar_reportes.py')
    else:
        generando = False
        logging.info("Generacion de reportes finalizada.")

    if manejador_db.restantes('enviado').cantidad > 0:
        os.system('/usr/local/bin/python3.9 /srv/www/vhosts/autoreportes_test/mandar_mails.py')
    else:
        enviando = False
        logging.info("Envio de mails finalizado.")
    
    time.sleep(1)

logging.info("FIN DE PROCESO.")