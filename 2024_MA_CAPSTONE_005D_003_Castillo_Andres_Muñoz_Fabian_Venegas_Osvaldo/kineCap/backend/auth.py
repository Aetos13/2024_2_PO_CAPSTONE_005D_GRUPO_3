from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend import db
from .models import User

auth_blueprint = Blueprint('auth', __name__)

# ------------------- Ruta de Registro de Usuarios ------------------- #
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Verificar si el email ya existe
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"message": "User already exists"}), 400
    
    # Hashear la contraseña usando pbkdf2:sha256
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Crear nuevo usuario
    new_user = User(
        nombre=data['nombre'],
        apellidos=data['apellidos'],
        telefono=data['telefono'],
        email=data['email'],
        pais=data['pais'],
        password=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully!"}), 201

# ------------------- Ruta de Login de Usuarios ------------------- #
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Buscar al usuario por email
    user = User.query.filter_by(email=data['email']).first()

    # Verificar si el usuario existe y si la contraseña es correcta
    if user and check_password_hash(user.password, data['password']):
        # Generar un token JWT si las credenciales son correctas
        token = create_access_token(identity=user.email)
        return jsonify({"token": token}), 200
    
    # Si no, retornar un mensaje de error
    return jsonify({"message": "Invalid credentials"}), 401

# ------------------- Ruta de Restablecimiento de Contraseña ------------------- #
@auth_blueprint.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    
    # Buscar el usuario por email
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Aquí es donde se implementaría la lógica para enviar un correo electrónico o SMS
    # Simulación de envío de correo
    return jsonify({"message": "Password reset link sent to your email"}), 200

# ------------------- Ruta de Actualización de Contraseña ------------------- #
@auth_blueprint.route('/update_password', methods=['PUT'])
@jwt_required()  # Requiere que el usuario esté autenticado
def update_password():
    # Obtener la identidad del token JWT
    current_user_email = get_jwt_identity()

    # Obtener la nueva contraseña desde la solicitud
    data = request.get_json()
    new_password = data['new_password']

    # Buscar al usuario actual
    user = User.query.filter_by(email=current_user_email).first()

    # Hashear la nueva contraseña
    hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

    # Actualizar la contraseña
    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password updated successfully!"}), 200
# ------------------- Ruta para Obtener Todos los Usuarios ------------------- #
@auth_blueprint.route('/users', methods=['GET'])
@jwt_required()  # Solo usuarios autenticados pueden acceder a esta ruta
def get_users():
    # Obtener todos los usuarios
    users = User.query.all()

    # Crear una lista con los datos de todos los usuarios
    users_data = []
    for user in users:
        user_info = {
            "nombre": user.nombre,
            "apellidos": user.apellidos,
            "telefono": user.telefono,
            "email": user.email,
            "pais": user.pais,
            "password": user.password  # Esta es la contraseña hasheada
        }
        users_data.append(user_info)

    return jsonify(users_data), 200