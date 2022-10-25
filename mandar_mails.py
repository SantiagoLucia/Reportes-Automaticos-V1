import email, smtplib, ssl, logging, os, time, manejador_db
from email import encoders
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import PORT, SMTP_SERVER, SENDER

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    filename='archivo.log', 
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%m-%y %H:%M:%S',
    level=logging.INFO
    )

port = PORT
smtp_server = SMTP_SERVER
sender = SENDER

envios = manejador_db.envios_pendientes()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_weekday = now.weekday()
current_day = now.day

#context = ssl.create_default_context()
#mailtrap no soporta ssl, con ssl agregar context=context
#with smtplib.SMTP(smtp_server,port) as server:
with smtplib.SMTP(smtp_server, port) as server:
    try:
        #server.starttls() #otra manera de asegurar la conexion
        #server.login(user, password)    

    #else:
        for envio in envios:

            id = envio[0]
            receiver = envio[1] 
            subject = envio[2]
            filename = envio[3]
            file_location = envio[4]
            periodicidad = envio[5]
            hora_ejecucion = envio[6]
            dia_semana = envio[7]
            dia_ejecucion = envio[8]

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

            if os.path.exists(file_location) == False:
                continue

            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = receiver
            message["Subject"] = subject

            body = "Este es un mail generado automaticamente por REPORTES DPMA, por favor no responder."
            message.attach(MIMEText(body, "plain"))

            with open(file_location, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}",
            )

            message.attach(part)
            text = message.as_string()

            server.sendmail(sender, receiver.split(','), text)
            time.sleep(1)
            manejador_db.modificar(id, 'enviado')
            logging.info(f"{filename} -> {receiver}")
        
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)