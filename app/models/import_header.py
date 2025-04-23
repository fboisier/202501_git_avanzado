from app.models.mysqlconnection import connectToMySQL
from datetime import datetime

class ImportHeader:
    def __init__(self, data):
        self.id = data.get('id')
        self.usuario_id = data.get('usuario_id')
        self.fecha_importacion = data.get('fecha_importacion')
        self.nombre_archivo = data.get('nombre_archivo')
        self.resumen_general = data.get('resumen_general')

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO import_headers (usuario_id, fecha_importacion, nombre_archivo, resumen_general)
        VALUES (%(usuario_id)s, %(fecha_importacion)s, %(nombre_archivo)s, %(resumen_general)s);
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM import_headers ORDER BY fecha_importacion DESC;"
        results = connectToMySQL().query_db(query)
        return [cls(row) for row in results]

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM import_headers WHERE id = %(id)s;"
        results = connectToMySQL().query_db(query, {'id': id})
        if results:
            return cls(results[0])
        return None
