from flask import Flask
import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Configuración de Bcrypt para el hash de contraseñas
bcrypt = Bcrypt(app)

# Importar controladores después de crear la aplicación para evitar importaciones circulares
from app.controllers import user_controller, visit_controller
from app.controllers.import_controller import bp as import_bp
app.register_blueprint(import_bp)