import smtplib
from flask import flash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class GmailMailer:
    def __init__(self, correo_emisor, contrasena_emisor):
        self.correo_emisor = correo_emisor
        self.contrasena_emisor = contrasena_emisor
        self.servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.servidor_smtp.starttls()
        self.servidor_smtp.login(correo_emisor, contrasena_emisor)

    def enviar_correo(self, correo_destino, asunto, cuerpo):
        try:
            mensaje = MIMEMultipart()
            mensaje['From'] = self.correo_emisor
            mensaje['To'] = correo_destino
            mensaje['Subject'] = asunto

            cuerpo_mensaje = cuerpo
            mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

            self.servidor_smtp.sendmail(self.correo_emisor, correo_destino, mensaje.as_string())
            return flash('Correo enviado correctamente. Pronto nos contactaremos contigo', 'success')
        except Exception as e:
            return flash('No se ha podido enviar el correo, intenta mas tarde', 'error')

    def cerrar_conexion(self):
        self.servidor_smtp.quit()