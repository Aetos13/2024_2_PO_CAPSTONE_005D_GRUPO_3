from flask import Flask, render_template, redirect, url_for, flash, session, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Configuraciones de seguridad y sesiones
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecretkey')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Conexión a la base de datos usando parámetros desde variables de entorno
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'Osvaldo21257'),
            database=os.getenv('DB_NAME', 'KiNE_CAP')
        )
    except Error as e:
        print(f'Error en la conexión a la base de datos: {e}')
        return None

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=50)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=50)])
    rol = SelectField('Rol', choices=[('estudiante', 'Estudiante'), ('administrador', 'Administrador')], validators=[InputRequired()])
    submit = SubmitField('Registrar')

class User(UserMixin):
    def __init__(self, id, rol):
        self.id = id
        self.rol = rol

@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT rol FROM usuario WHERE id_usuario = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()

    if user_data:
        return User(user_id, user_data[0])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        connection = get_db_connection()
        if connection is None:
            flash('No se pudo conectar a la base de datos.')
            return render_template('login.html', form=form)

        cursor = connection.cursor()
        cursor.execute("SELECT id_usuario, contraseña, rol FROM usuario WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if user_data and check_password_hash(user_data[1], password):
            user = User(user_data[0], user_data[2])
            login_user(user)
            flash('¡Sesión iniciada exitosamente!')
            return redirect(url_for('admin_dashboard') if user.rol == 'administrador' else url_for('student_dashboard'))
        
        flash('Correo o contraseña incorrectos.')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        rol = form.rol.data

        connection = get_db_connection()
        if connection is None:
            flash('No se pudo conectar a la base de datos.')
            return render_template('register.html', form=form)

        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO usuario (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)", 
                           (nombre, email, password, rol))
            connection.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Error al registrar el usuario: {err}')
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def student_dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

# Nuevas rutas para recursos y inscripción a cursos
@app.route('/curso/<int:curso_id>/recurso', methods=['POST'])
@login_required
def agregar_recurso(curso_id):
    titulo = request.json.get('titulo')
    url = request.json.get('url')
    tipo = request.json.get('tipo')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"message": "No se pudo conectar a la base de datos."}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Recurso (id_curso, titulo, url, tipo) VALUES (%s, %s, %s, %s)", 
                       (curso_id, titulo, url, tipo))
        connection.commit()
        return jsonify({"message": "Recurso agregado exitosamente!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": f"Error al agregar recurso: {err}"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/curso/<int:curso_id>/recursos', methods=['GET'])
@login_required
def listar_recursos(curso_id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"message": "No se pudo conectar a la base de datos."}), 500

    cursor = connection.cursor()
    cursor.execute("SELECT id_recurso, titulo, url, tipo FROM Recurso WHERE id_curso = %s", (curso_id,))
    recursos = cursor.fetchall()
    cursor.close()
    connection.close()

    recursos_list = [{"id": r[0], "titulo": r[1], "url": r[2], "tipo": r[3]} for r in recursos]
    return jsonify(recursos_list)

@app.route('/curso/<int:curso_id>/inscribir', methods=['POST'])
@login_required
def inscribir_curso(curso_id):
    user_id = current_user.id

    connection = get_db_connection()
    if connection is None:
        return jsonify({"message": "No se pudo conectar a la base de datos."}), 500

    cursor = connection.cursor()
    # Verificar si el usuario ya está inscrito en el curso
    cursor.execute("SELECT * FROM Progreso WHERE id_usuario = %s AND id_curso = %s", (user_id, curso_id))
    progreso_existente = cursor.fetchone()

    if progreso_existente:
        return jsonify({"message": "Ya estás inscrito en este curso."}), 400

    try:
        cursor.execute("INSERT INTO Progreso (id_usuario, id_curso, porcentaje) VALUES (%s, %s, %s)", 
                       (user_id, curso_id, 0))  # Comenzar con 0% de progreso
        connection.commit()
        return jsonify({"message": "Inscripción exitosa!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": f"Error al inscribir al curso: {err}"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
