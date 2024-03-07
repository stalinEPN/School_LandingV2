from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from config import config
import psycopg2
import os
#import base64

#Models
from models.ModelPersona import ModelPersona

#Entities
from models.entities.Persona import Persona

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():

    return render_template('views/home.html')

@app.route('/changes')
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
    persona = Persona(
        id=request.form.get('id'),
        cargo='',
        nombre=request.form.get('Nombre'),
        apellido=request.form.get('Apellido'),
        descripcion=request.form.get('Descripcion'),
        foto=psycopg2.Binary((request.files['Foto']).read()) 
    )

    if persona.foto is None:
        ModelPersona.edit_persona_Nofoto(persona)
    else:
        ModelPersona.edit_persona_foto(persona)

    return redirect(url_for('changes'))
    




@app.errorhandler(404)
def status_404(error):
    return render_template('views/404.html')

if __name__ == '__main__':
    
    app.config.from_object(config['development'])
    app.register_error_handler(404, status_404)

    app.run(debug=True)
