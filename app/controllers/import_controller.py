from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
import csv
from datetime import datetime
from app.models.import_header import ImportHeader
from app.models.import_detail import ImportDetail
from app.models.user import User  # Asumiendo que tienes este modelo
from app.models.visit import Visit  # Usar Visit para validar existencia de parque y crear visitas

bp = Blueprint('import', __name__)

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = 'app/static/uploads/imports/'

# Asegura que el directorio exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/importar_visitas', methods=['GET', 'POST'])
def importar_visitas():
    if request.method == 'GET':
        return render_template('importar_visitas.html')

    if 'file' not in request.files:
        flash('No se adjuntó ningún archivo', 'danger')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('Archivo no seleccionado', 'danger')
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash('Tipo de archivo no permitido', 'danger')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    usuario_id = session.get('user_id')
    if not usuario_id:
        flash('Debes estar logeado para importar', 'danger')
        return redirect(url_for('login'))

    resumen = []
    total_ok = 0
    total_error = 0
    detalles = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for i, row in enumerate(reader, start=2):  # Empieza en 2 por el header
            nombre = row.get('Nombre', '').strip()
            fecha_str = row.get('Fecha', '').strip()
            rating_str = row.get('Rating', '').strip()
            comentarios = row.get('Comentarios', '').strip()
            resultado = 'OK'
            mensaje_error = ''
            # Validaciones
            if not nombre:
                resultado = 'ERROR'
                mensaje_error = 'Nombre de parque vacío'
            # Aquí asumimos que tienes una lista o tabla de parques válidos. Si no, puedes omitir esta validación.
            # Si quieres validar solo por nombres únicos registrados en visitas, puedes consultar la tabla de parques si existe.
            # Por ahora, validamos que el nombre no esté vacío.

            try:
                fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
            except Exception:
                resultado = 'ERROR'
                mensaje_error = 'Fecha inválida'
                fecha = None
            try:
                rating = int(rating_str)
                if rating < 1 or rating > 5:
                    raise ValueError()
            except Exception:
                resultado = 'ERROR'
                mensaje_error = 'Rating inválido (debe ser 1 a 5)'
                rating = None
            if resultado == 'OK':
                # Crear la visita
                Visit.create({
                    'park_name': nombre,
                    'date': fecha.strftime('%Y-%m-%d'),
                    'rating': rating,
                    'comments': comentarios,
                    'photo_path': None,
                    'user_id': usuario_id
                })
                total_ok += 1
            else:
                total_error += 1
            detalles.append({
                'linea_numero': i,
                'nombre': nombre,
                'fecha': fecha,
                'rating': rating,
                'comentarios': comentarios,
                'resultado': resultado,
                'mensaje_error': mensaje_error
            })
    # Guarda encabezado
    header_id = ImportHeader.save({
        'usuario_id': usuario_id,
        'fecha_importacion': datetime.now(),
        'nombre_archivo': filename,
        'resumen_general': f'OK: {total_ok}, ERROR: {total_error}'
    })
    # Guarda detalles
    for det in detalles:
        ImportDetail.save({
            'import_header_id': header_id,
            'linea_numero': det['linea_numero'],
            'nombre': det['nombre'],
            'fecha': det['fecha'],
            'rating': det['rating'],
            'comentarios': det['comentarios'],
            'resultado': det['resultado'],
            'mensaje_error': det['mensaje_error']
        })
    return render_template('importar_resumen.html', detalles=detalles, total_ok=total_ok, total_error=total_error)

@bp.route('/importaciones')
def lista_importaciones():
    usuario_id = session.get('user_id')
    if not usuario_id:
        flash('Debes estar logeado para ver las importaciones', 'danger')
        return redirect(url_for('login'))
    headers = ImportHeader.get_all()
    return render_template('importaciones.html', headers=headers)

@bp.route('/importaciones/<int:header_id>')
def detalle_importacion(header_id):
    usuario_id = session.get('user_id')
    if not usuario_id:
        flash('Debes estar logeado para ver los detalles', 'danger')
        return redirect(url_for('login'))
    header = ImportHeader.get_by_id(header_id)
    detalles = ImportDetail.get_by_header(header_id)
    return render_template('importacion_detalle.html', header=header, detalles=detalles)
