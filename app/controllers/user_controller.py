from flask import render_template, redirect, request, session, flash
from app import app, bcrypt
from app.models.user import User
from flask_bcrypt import Bcrypt

# Ruta para la página de inicio (login y registro)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

# Ruta para procesar el registro de usuarios
@app.route('/register', methods=['POST'])
def register():
    # Validar los datos del formulario
    if not User.validate_registration(request.form):
        return redirect('/')
    
    # Crear hash de la contraseña
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    # Crear diccionario con los datos del usuario
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    
    # Guardar usuario y obtener ID
    user_id = User.create(data)
    
    # Guardar ID de usuario en sesión
    session['user_id'] = user_id
    session['user_name'] = f"{request.form['first_name']} {request.form['last_name']}"
    
    return redirect('/dashboard')

# Ruta para procesar el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    # Validar email y obtener usuario
    is_valid, user_in_db = User.validate_login(request.form)
    
    if not is_valid:
        return redirect('/')
    
    # Verificar contraseña
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Email o contraseña incorrectos", "login")
        return redirect('/')
    
    # Guardar datos de usuario en sesión
    session['user_id'] = user_in_db.id
    session['user_name'] = f"{user_in_db.first_name} {user_in_db.last_name}"
    
    return redirect('/dashboard')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')