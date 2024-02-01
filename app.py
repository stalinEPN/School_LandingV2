from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():

    return render_template('views/home.html')


def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return render_template('views/404.html')

if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    app.run()
