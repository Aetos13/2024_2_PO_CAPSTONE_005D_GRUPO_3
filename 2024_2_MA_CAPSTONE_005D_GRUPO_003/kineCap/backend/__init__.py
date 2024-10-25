from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Admin_KineCap:1234@localhost/KineCap_DB'
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    
    # Inicializar las extensiones
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # Registrar blueprints
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app