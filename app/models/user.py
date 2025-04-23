from app.models.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "parques_db"
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # Método para obtener todos los usuarios
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL().query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    # Método para crear un nuevo usuario
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL().query_db(query, data)
    
    # Método para buscar un usuario por ID
    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {"id": user_id}
        results = connectToMySQL().query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    # Método para buscar un usuario por email
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        results = connectToMySQL().query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    # Método para validar el registro de usuario
    @staticmethod
    def validate_registration(user):
        is_valid = True
        
        # Validar que el nombre y apellido tengan al menos 2 caracteres
        if len(user['first_name']) < 2:
            flash("El nombre debe tener al menos 2 caracteres", "register")
            is_valid = False
        
        if len(user['last_name']) < 2:
            flash("El apellido debe tener al menos 2 caracteres", "register")
            is_valid = False
        
        # Validar formato de email
        if not EMAIL_REGEX.match(user['email']):
            flash("Email inválido", "register")
            is_valid = False
        
        # Verificar si el email ya existe en la base de datos
        if User.get_by_email(user['email']):
            flash("Este email ya está registrado", "register")
            is_valid = False
        
        # Validar longitud de contraseña
        if len(user['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", "register")
            is_valid = False
        
        # Validar que las contraseñas coincidan
        if user['password'] != user['confirm_password']:
            flash("Las contraseñas no coinciden", "register")
            is_valid = False
        
        return is_valid
    
    # Método para validar el login
    @staticmethod
    def validate_login(user):
        is_valid = True
        
        # Verificar que el email existe
        user_in_db = User.get_by_email(user['email'])
        if not user_in_db:
            flash("Email o contraseña incorrectos", "login")
            is_valid = False
        
        return is_valid, user_in_db