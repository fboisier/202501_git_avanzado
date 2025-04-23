import pymysql.cursors
import os
from dotenv import load_dotenv

# Cargar variables de entorno (asegurarse de que se cargue desde la ruta correcta)
load_dotenv()

# Imprimir valores para depuración (solo en desarrollo)
if os.environ.get('DEBUG') == 'True':
    print(f"MYSQL_HOST: {os.environ.get('MYSQL_HOST', 'no definido')}")
    print(f"MYSQL_USER: {os.environ.get('MYSQL_USER', 'no definido')}")
    print(f"MYSQL_DB: {os.environ.get('MYSQL_DB', 'no definido')}")
    print(f"MYSQL_PORT: {os.environ.get('MYSQL_PORT', 'no definido')}")

# Esta clase se encargará de conectar con nuestra base de datos
class MySQLConnection:
    def __init__(self):
        # Obtener valores con valores predeterminados como respaldo
        host = os.environ.get('MYSQL_HOST', 'localhost')
        user = os.environ.get('MYSQL_USER', 'root')
        password = os.environ.get('MYSQL_PASSWORD', '')
        db = os.environ.get('MYSQL_DB', 'parques_db')
        port = int(os.environ.get('MYSQL_PORT', 3306))
        
        # Imprimir los valores que se están usando (solo en desarrollo)
        if os.environ.get('DEBUG') == 'True':
            print(f"Conectando a MySQL con: Host={host}, User={user}, DB={db}, Port={port}")
        
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.cursor = self.connection.cursor()
    
    def query_db(self, query, data=None):
        try:
            self.cursor.execute(query, data)
            if query.lower().find("insert") >= 0:
                # Retorna el ID del nuevo registro
                return self.cursor.lastrowid
            elif query.lower().find("select") >= 0:
                # Retorna los datos seleccionados
                return self.cursor.fetchall()
            else:
                # Si es un UPDATE o DELETE retorna nada
                return None
        except Exception as e:
            print(f"Error en la consulta: {e}")
            return False
        finally:
            self.connection.close()

# Función para conectar con la base de datos
def connectToMySQL():
    return MySQLConnection()