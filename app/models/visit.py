from app.models.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
from app.models.user import User

class Visit:
    db = "parques_db"
    
    def __init__(self, data):
        self.id = data['id']
        self.park_name = data['park_name']
        self.date = data['date']
        self.rating = data['rating']
        self.comments = data['comments']
        self.photo_path = data['photo_path'] if 'photo_path' in data else None
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.likes_count = 0
        self.liked_by_user = False
    
    # Método para obtener todas las visitas con información del usuario asociado
    @classmethod
    def get_all_with_users(cls):
        query = """
            SELECT visits.*, users.first_name, users.last_name, users.email,
            COUNT(DISTINCT likes.id) as likes_count
            FROM visits
            JOIN users ON visits.user_id = users.id
            LEFT JOIN likes ON visits.id = likes.visit_id
            GROUP BY visits.id
            ORDER BY visits.rating DESC;
        """
        results = connectToMySQL().query_db(query)
        all_visits = []
        
        for row in results:
            visit = cls(row)
            
            user_data = {
                "id": row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "",
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            
            visit.user = User(user_data)
            visit.likes_count = row['likes_count']
            all_visits.append(visit)
            
        return all_visits
    
    # Método para obtener visitas de un usuario específico
    @classmethod
    def get_by_user_id(cls, user_id):
        query = """
            SELECT visits.*, COUNT(DISTINCT likes.id) as likes_count
            FROM visits
            LEFT JOIN likes ON visits.id = likes.visit_id
            WHERE visits.user_id = %(user_id)s
            GROUP BY visits.id
            ORDER BY visits.rating DESC;
        """
        data = {"user_id": user_id}
        results = connectToMySQL().query_db(query, data)
        
        visits = []
        for row in results:
            visit = cls(row)
            visit.likes_count = row['likes_count']
            visits.append(visit)
            
        return visits
    
    # Método para obtener visitas de otros usuarios
    @classmethod
    def get_other_users_visits(cls, user_id):
        query = """
            SELECT visits.*, users.first_name, users.last_name, users.email,
            COUNT(DISTINCT likes.id) as likes_count
            FROM visits
            JOIN users ON visits.user_id = users.id
            LEFT JOIN likes ON visits.id = likes.visit_id
            WHERE visits.user_id != %(user_id)s
            GROUP BY visits.id
            ORDER BY visits.rating DESC;
        """
        data = {"user_id": user_id}
        results = connectToMySQL().query_db(query, data)
        
        visits = []
        for row in results:
            visit = cls(row)
            
            user_data = {
                "id": row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "",
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            
            visit.user = User(user_data)
            visit.likes_count = row['likes_count']
            visits.append(visit)
            
        return visits
    
    # Método para obtener una visita por ID
    @classmethod
    def get_by_id(cls, visit_id, user_id=None):
        query = """
            SELECT visits.*, users.first_name, users.last_name, users.email,
            COUNT(DISTINCT likes.id) as likes_count,
            MAX(CASE WHEN likes.user_id = %(user_id)s THEN 1 ELSE 0 END) as liked_by_user
            FROM visits
            JOIN users ON visits.user_id = users.id
            LEFT JOIN likes ON visits.id = likes.visit_id
            WHERE visits.id = %(visit_id)s
            GROUP BY visits.id;
        """
        data = {
            "visit_id": visit_id,
            "user_id": user_id if user_id else 0
        }
        results = connectToMySQL().query_db(query, data)
        
        if len(results) < 1:
            return False
        
        row = results[0]
        visit = cls(row)
        
        user_data = {
            "id": row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "password": "",
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
        
        visit.user = User(user_data)
        visit.likes_count = row['likes_count']
        visit.liked_by_user = bool(row['liked_by_user'])
        
        return visit
    
    # Método para crear una nueva visita
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO visits (park_name, date, rating, comments, photo_path, user_id) 
            VALUES (%(park_name)s, %(date)s, %(rating)s, %(comments)s, %(photo_path)s, %(user_id)s);
        """
        return connectToMySQL().query_db(query, data)
    
    # Método para actualizar una visita
    @classmethod
    def update(cls, data):
        query = """
            UPDATE visits 
            SET park_name = %(park_name)s, date = %(date)s, 
                rating = %(rating)s, comments = %(comments)s
        """
        
        # Si hay una nueva foto, actualizarla
        if 'photo_path' in data and data['photo_path']:
            query += ", photo_path = %(photo_path)s"
        
        query += " WHERE id = %(id)s;"
        
        return connectToMySQL().query_db(query, data)
    
    # Método para eliminar una visita
    @classmethod
    def delete(cls, visit_id):
        # Primero eliminar los likes asociados
        query_likes = "DELETE FROM likes WHERE visit_id = %(visit_id)s;"
        data = {"visit_id": visit_id}
        connectToMySQL().query_db(query_likes, data)
        
        # Luego eliminar la visita
        query = "DELETE FROM visits WHERE id = %(visit_id)s;"
        return connectToMySQL().query_db(query, data)
    
    # Método para verificar si un usuario ya ha registrado un parque específico
    @classmethod
    def park_exists_for_user(cls, park_name, user_id, visit_id=None):
        if visit_id:
            # Si estamos editando, excluimos la visita actual
            query = """
                SELECT * FROM visits 
                WHERE park_name = %(park_name)s AND user_id = %(user_id)s AND id != %(visit_id)s;
            """
            data = {
                "park_name": park_name,
                "user_id": user_id,
                "visit_id": visit_id
            }
        else:
            # Si estamos creando una nueva visita
            query = """
                SELECT * FROM visits 
                WHERE park_name = %(park_name)s AND user_id = %(user_id)s;
            """
            data = {
                "park_name": park_name,
                "user_id": user_id
            }
        
        results = connectToMySQL().query_db(query, data)
        return len(results) > 0
    
    # Método para dar like a una visita
    @classmethod
    def add_like(cls, visit_id, user_id):
        # Verificar si ya dio like
        query_check = """
            SELECT * FROM likes 
            WHERE visit_id = %(visit_id)s AND user_id = %(user_id)s;
        """
        data = {
            "visit_id": visit_id,
            "user_id": user_id
        }
        results = connectToMySQL().query_db(query_check, data)
        
        if len(results) > 0:
            # Ya dio like, no hacer nada
            return False
        
        # Añadir like
        query = """
            INSERT INTO likes (visit_id, user_id) 
            VALUES (%(visit_id)s, %(user_id)s);
        """
        return connectToMySQL().query_db(query, data)
    
    # Método para validar los datos de visita
    @staticmethod
    def validate_visit(data, is_new=True, user_id=None):
        is_valid = True
        
        # Validar que los campos no estén vacíos
        if len(data['park_name']) < 1:
            flash("El nombre del parque no puede estar vacío", "visit")
            is_valid = False
        
        if not data['date']:
            flash("La fecha es obligatoria", "visit")
            is_valid = False
        else:
            # Validar que la fecha no sea futura
            try:
                visit_date = datetime.strptime(data['date'], '%Y-%m-%d')
                today = datetime.now()
                if visit_date > today:
                    flash("No puedes registrar visitas futuras", "visit")
                    is_valid = False
            except ValueError:
                flash("Formato de fecha inválido", "visit")
                is_valid = False
        
        try:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                flash("El rating debe ser un número entre 1 y 5", "visit")
                is_valid = False
        except ValueError:
            flash("El rating debe ser un número", "visit")
            is_valid = False
        
        if len(data['comments']) < 1:
            flash("Los comentarios no pueden estar vacíos", "visit")
            is_valid = False
        
        # Validar que el parque sea único para ese usuario (solo en creación)
        if is_new and user_id:
            if Visit.park_exists_for_user(data['park_name'], user_id):
                flash("Ya has registrado una visita para este parque", "visit")
                is_valid = False
        elif not is_new and 'id' in data and user_id:
            # En edición, verificar si ya existe otro registro con el mismo parque
            if Visit.park_exists_for_user(data['park_name'], user_id, data['id']):
                flash("Ya has registrado una visita para este parque", "visit")
                is_valid = False
        
        return is_valid