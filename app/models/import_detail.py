from app.models.mysqlconnection import connectToMySQL

class ImportDetail:
    def __init__(self, data):
        self.id = data.get('id')
        self.import_header_id = data.get('import_header_id')
        self.linea_numero = data.get('linea_numero')
        self.nombre = data.get('nombre')
        self.fecha = data.get('fecha')
        self.rating = data.get('rating')
        self.comentarios = data.get('comentarios')
        self.resultado = data.get('resultado')
        self.mensaje_error = data.get('mensaje_error')

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO import_details (import_header_id, linea_numero, nombre, fecha, rating, comentarios, resultado, mensaje_error)
        VALUES (%(import_header_id)s, %(linea_numero)s, %(nombre)s, %(fecha)s, %(rating)s, %(comentarios)s, %(resultado)s, %(mensaje_error)s);
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def get_by_header(cls, import_header_id):
        query = "SELECT * FROM import_details WHERE import_header_id = %(import_header_id)s ORDER BY linea_numero;"
        results = connectToMySQL().query_db(query, {'import_header_id': import_header_id})
        return [cls(row) for row in results]
