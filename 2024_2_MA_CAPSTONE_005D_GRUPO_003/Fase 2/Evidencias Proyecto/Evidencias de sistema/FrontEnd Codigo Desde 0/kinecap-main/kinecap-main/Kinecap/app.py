from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Configuración de Flask-CORS
CORS(app, supports_credentials=True)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Usuario simulado (usaremos un usuario ficticio por ahora)
users = {'test@example.com': {'password': 'password123'}}

# Clase User que hereda de UserMixin, necesaria para manejar usuarios con Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Cargar el usuario por su id (en este caso el email)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Rutas para React (Frontend)
@app.route('/')
@app.route('/<path:path>')
def serve_react(path=''):
    # React se encarga de manejar las rutas del frontend
    return render_template('index.html')

# API para el login
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Verificar si el email existe en nuestro diccionario y la contraseña coincide
    if email in users and users[email]['password'] == password:
        user = User(email)
        login_user(user)
        return jsonify({'message': 'Login exitoso.', 'user': email}), 200

    return jsonify({'message': 'Correo o contraseña incorrectos.'}), 401

# API para logout
@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Has cerrado sesión correctamente.'}), 200

# API protegida (ejemplo del dashboard)
@app.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard():
    return jsonify({'message': f'Bienvenido {current_user.id} al dashboard.'}), 200

# Ruta adicional para "Sobre Nosotros"
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta adicional para "Cursos"
@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

if __name__ == '__main__':
    app.run(debug=True)
