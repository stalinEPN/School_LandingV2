from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from config import config
import os

app = Flask(__name__)

#directorio donde se almacenaran las imagenes
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def imagen_formatos(filename):
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():

    return render_template('views/home.html')

@app.route('/changes')
def changes():
    return render_template('views/changes.html')

@app.route('/save-img', methods=['POST'])
def saveImg():
    if request.method == 'POST':
        # Verifica si se ha enviado un archivo
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo')
            return redirect(url_for('changes'))
        
        file = request.files['file']

        # Verifica si el archivo tiene un nombre y la extensión permitida
        if file.filename == '':
            flash('No se seleccionó ningún archivo')
            return redirect(url_for('changes'))
        
        if file and imagen_formatos(file.filename):
            # Guarda el archivo en el directorio UPLOAD_FOLDER
            filename = 'rector.png'  # Mantén el nombre igual al archivo original
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Imagen reemplazada con éxito', 'success')
            return redirect(url_for('changes'))


@app.errorhandler(404)
def status_404(error):
    return render_template('views/404.html')

if __name__ == '__main__':
    
    app.config.from_object(config['development'])
    app.register_error_handler(404, status_404)


    app.run(debug=True)
