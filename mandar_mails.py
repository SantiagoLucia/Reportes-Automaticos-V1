import smtplib, logging, os, time, manejador_db
from email import encoders
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    filename='archivo.log', 
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%m-%y %H:%M:%S',
    level=logging.INFO
    )

port = 25
smtp_server = "localhost"
sender = "<no-responder@devdpma.gdeba.gba.gob.ar>"

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_weekday = now.weekday()
current_day = now.day


def para_ejecutar(envio):
    if envio.periodicidad == "DIARIO":
        if datetime.strptime(envio.hora_ejecucion,"%H:%M:%S") > datetime.strptime(current_time,"%H:%M:%S"):
            return False

    if envio.periodicidad == "SEMANAL":
        if current_weekday == envio.dia_semana:
            if datetime.strptime(envio.hora_ejecucion,"%H:%M:%S") > datetime.strptime(current_time,"%H:%M:%S"):
                return False 
        else:
            manejador_db.modificar(envio.id, 'generado')
            manejador_db.modificar(envio.id, 'enviado')
            return False

    if envio.periodicidad == "MENSUAL":
        if current_day == envio.dia_ejecucion:
            if datetime.strptime(envio.hora_ejecucion,"%H:%M:%S") > datetime.strptime(current_time,"%H:%M:%S"):
                return False 
        else:
            manejador_db.modificar(envio.id, 'generado')
            manejador_db.modificar(envio.id, 'enviado')
            return False     

    return True


def mandar_mail(server, envio):
    message = MIMEMultipart()
    message["From"] = envio.sender
    message["To"] = envio.receiver
    message["Subject"] = envio.subject
    message["Cc"] = envio.receiver_cc
    
    to = envio.receiver.split(',')

    if envio.receiver_cc:
        to += envio.receiver_cc.split(',')

    if envio.receiver_cco:
        to += envio.receiver_cco.split(',')

    body = "Este es un mail generado automaticamente por REPORTES DPMA, por favor no responder."
    message.attach(MIMEText(body, "plain"))

    with open(envio.file_location, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    nombre = envio.filename.replace('.xlsx', '-'+now.strftime('%d_%m_%Y_%H_%M')+'.xlsx')

    part.add_header(
        "Content-Disposition",
        f"attachment; filename={nombre}",
    )

    message.attach(part)
    text = message.as_string()
    server.sendmail(envio.sender, to, text)    


if __name__ == '__main__':
    
    with smtplib.SMTP(smtp_server, port) as server:
        try:
            for envio in manejador_db.envios_pendientes():

                if not para_ejecutar(envio):
                    continue

                if os.path.exists(envio.file_location) == False:
                    continue

                mandar_mail(server, envio)
                time.sleep(1)
                
                manejador_db.modificar(id, 'enviado')
                logging.info(f"{envio.filename} -> {envio.receiver} CC: {envio.receiver_cc} CCO: {envio.receiver_cco}")
            
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)