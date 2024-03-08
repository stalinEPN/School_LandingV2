from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import config
import psycopg2

#Models
from models.ModelPersona import ModelPersona

#Entities
from models.entities.Persona import Persona

#apis
from api.GmailMailer import GmailMailer

app = Flask(__name__)
app.secret_key = 'B!1weNAt1T^%kvhUI*S^'

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    personas = ModelPersona.get_personas()
    return render_template('views/home.html', personas=personas)

@app.route('/changes', methods=['GET','POST'])
def changes():
    try:
        personas = ModelPersona.get_personas()
        return render_template('views/changes.html', personas=personas)
    except Exception as ex:
        # Manejar la excepción según tus necesidades
        #return render_template('views/404.html')
        raise Exception(ex)
    
@app.route('/editar', methods=['POST'])
def editar_persona():

    nuevaFoto = request.files['Foto']

    persona = Persona(
        id=request.form.get('id'),
        cargo='',
        nombre=request.form.get('Nombre'),
        apellido=request.form.get('Apellido'),
        descripcion=request.form.get('Descripcion'),
        foto=None
    )

    if nuevaFoto.filename != '':
        persona.foto = psycopg2.Binary(nuevaFoto.read())

    if persona.foto is None:
        ModelPersona.edit_persona_Nofoto(persona)
    else:
        ModelPersona.edit_persona_foto(persona)

    return redirect(url_for('changes'))

@app.route('/contactos', methods=['GET','POST'])
def enviar_email():
    sender = GmailMailer('school.exampleepn@gmail.com', 'empm sgha qhvw asmu')
    name = request.form.get('name')
    yemail = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    mail_body = f"""
                Nombre del remitente: {name}
                Email del remitente: {yemail}
                Razon: {subject}
                Mensaje: \n\n{message}
                """
    
    sender.enviar_correo('school.exampleepn@gmail.com', subject, mail_body)
    
    return redirect(url_for('home')+'#contact')

@app.errorhandler(404)
def status_404(error):
    return render_template('views/404.html')

if __name__ == '__main__':
    
    app.config.from_object(config['development'])
    
    app.register_error_handler(404, status_404)

    app.run(debug=True)
