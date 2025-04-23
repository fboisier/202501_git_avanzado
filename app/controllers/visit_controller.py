from flask import render_template, redirect, request, session, flash, make_response
from app import app
from app.models.visit import Visit
from app.models.user import User
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Configuración para la carga de imágenes
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Función para verificar si la extensión del archivo es válida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función de decorador para verificar si el usuario está en sesión
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Ruta para el dashboard principal
@app.route('/dashboard')
@login_required
def dashboard():
    # Obtener el usuario actual
    user = User.get_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect('/')
    
    # Obtener las visitas del usuario actual
    user_visits = Visit.get_by_user_id(session['user_id'])
    
    # Obtener las visitas de otros usuarios
    other_visits = Visit.get_other_users_visits(session['user_id'])
    
    return render_template(
        'dashboard.html',
        user_name=session['user_name'],
        user_visits=user_visits,
        other_visits=other_visits
    )

# Ruta para mostrar el formulario de creación de visita
@app.route('/visits/new')
@login_required
def new_visit():
    return render_template('new_visit.html')

# Ruta para procesar la creación de una visita
@app.route('/visits/create', methods=['POST'])
@login_required
def create_visit():
    # Validar los datos del formulario
    if not Visit.validate_visit(request.form, True, session['user_id']):
        return redirect('/visits/new')
    
    # Crear diccionario con los datos de la visita
    data = {
        "park_name": request.form['park_name'],
        "date": request.form['date'],
        "rating": request.form['rating'],
        "comments": request.form['comments'],
        "photo_path": None,
        "user_id": session['user_id']
    }
    
    # Procesar la foto si se proporciona
    if 'photo' in request.files and request.files['photo'].filename != '':
        photo = request.files['photo']
        if allowed_file(photo.filename):
            # Crear un nombre único para la imagen
            filename = secure_filename(photo.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Guardar la imagen
            photo_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            photo.save(photo_path)
            
            # Guardar la ruta relativa en la base de datos
            data["photo_path"] = unique_filename
        else:
            flash("Formato de imagen no válido. Se permiten: png, jpg, jpeg, gif", "visit")
            return redirect('/visits/new')
    
    # Guardar visita en la base de datos
    Visit.create(data)
    
    return redirect('/dashboard')

# Ruta para ver una visita específica
@app.route('/visits/<int:visit_id>')
@login_required
def show_visit(visit_id):
    # Obtener la visita
    visit = Visit.get_by_id(visit_id, session['user_id'])
    
    if not visit:
        flash("Visita no encontrada", "error")
        return redirect('/dashboard')
    
    return render_template('show_visit.html', visit=visit)

# Ruta para mostrar el formulario de edición de visita
@app.route('/visits/edit/<int:visit_id>')
@login_required
def edit_visit(visit_id):
    # Obtener la visita
    visit = Visit.get_by_id(visit_id)
    
    if not visit:
        flash("Visita no encontrada", "error")
        return redirect('/dashboard')
    
    # Verificar que el usuario actual sea el propietario de la visita
    if visit.user_id != session['user_id']:
        flash("No tienes permiso para editar esta visita", "error")
        return redirect('/dashboard')
    
    return render_template('edit_visit.html', visit=visit)

# Ruta para procesar la actualización de una visita
@app.route('/visits/update/<int:visit_id>', methods=['POST'])
@login_required
def update_visit(visit_id):
    # Obtener la visita
    visit = Visit.get_by_id(visit_id)
    
    if not visit:
        flash("Visita no encontrada", "error")
        return redirect('/dashboard')
    
    # Verificar que el usuario actual sea el propietario de la visita
    if visit.user_id != session['user_id']:
        flash("No tienes permiso para editar esta visita", "error")
        return redirect('/dashboard')
    
    # Validar los datos del formulario
    data = {
        "id": visit_id,
        "park_name": request.form['park_name'],
        "date": request.form['date'],
        "rating": request.form['rating'],
        "comments": request.form['comments']
    }
    
    if not Visit.validate_visit(data, False, session['user_id']):
        return redirect(f'/visits/edit/{visit_id}')
    
    # Procesar la foto si se proporciona
    if 'photo' in request.files and request.files['photo'].filename != '':
        photo = request.files['photo']
        if allowed_file(photo.filename):
            # Eliminar la foto anterior si existe
            if visit.photo_path:
                old_photo_path = os.path.join(UPLOAD_FOLDER, visit.photo_path)
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            
            # Crear un nombre único para la nueva imagen
            filename = secure_filename(photo.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Guardar la nueva imagen
            photo_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            photo.save(photo_path)
            
            # Guardar la ruta relativa en la base de datos
            data["photo_path"] = unique_filename
        else:
            flash("Formato de imagen no válido. Se permiten: png, jpg, jpeg, gif", "visit")
            return redirect(f'/visits/edit/{visit_id}')
    
    # Actualizar visita en la base de datos
    Visit.update(data)
    
    return redirect('/dashboard')

# Ruta para eliminar una visita
@app.route('/visits/delete/<int:visit_id>')
@login_required
def delete_visit(visit_id):
    # Obtener la visita
    visit = Visit.get_by_id(visit_id)
    
    if not visit:
        flash("Visita no encontrada", "error")
        return redirect('/dashboard')
    
    # Verificar que el usuario actual sea el propietario de la visita
    if visit.user_id != session['user_id']:
        flash("No tienes permiso para eliminar esta visita", "error")
        return redirect('/dashboard')
    
    # Eliminar la foto si existe
    if visit.photo_path:
        photo_path = os.path.join(UPLOAD_FOLDER, visit.photo_path)
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    # Eliminar visita de la base de datos
    Visit.delete(visit_id)
    
    flash("Visita eliminada correctamente", "success")
    return redirect('/dashboard')

# Ruta para dar like a una visita
@app.route('/visits/like/<int:visit_id>')
@login_required
def like_visit(visit_id):
    # Verificar que la visita exista
    visit = Visit.get_by_id(visit_id, session['user_id'])
    
    if not visit:
        flash("Visita no encontrada", "error")
        return redirect('/dashboard')
    
    # No permitir dar like a sus propias visitas
    if visit.user_id == session['user_id']:
        flash("No puedes dar like a tus propias visitas", "error")
        return redirect('/dashboard')
    
    # Verificar si ya dio like
    if visit.liked_by_user:
        flash("Ya has dado like a esta visita", "error")
        return redirect('/dashboard')
    
    # Añadir like
    Visit.add_like(visit_id, session['user_id'])
    
    return redirect(f'/visits/{visit_id}')

# Ruta para generar PDF con el resumen de la visita
@app.route('/visits/<int:visit_id>/pdf')
@login_required
def generate_visit_pdf(visit_id):
    # Obtener la visita
    visit = Visit.get_by_id(visit_id, session['user_id'])
    
    if not visit:
        flash("Visita no encontrada", "error")
        return redirect('/dashboard')
    
    # Crear un buffer para almacenar el PDF
    buffer = BytesIO()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos para el PDF
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,
        spaceAfter=12
    )
    
    # Título del documento
    title = Paragraph(f"Resumen de Visita al Parque {visit.park_name}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Información básica
    elements.append(Paragraph(f"<b>Visitante:</b> {visit.user.first_name} {visit.user.last_name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Fecha de visita:</b> {visit.date}", styles["Normal"]))
    
    # Rating con estrellas
    rating_text = f"<b>Rating:</b> {visit.rating}/5 "
    rating_text += "★" * int(visit.rating)
    elements.append(Paragraph(rating_text, styles["Normal"]))
    elements.append(Spacer(1, 10))
    
    # Agregar la imagen si existe
    if visit.photo_path:
        try:
            img_path = os.path.join(UPLOAD_FOLDER, visit.photo_path)
            if os.path.exists(img_path):
                img = Image(img_path, width=300, height=200, kind='proportional')
                elements.append(img)
                elements.append(Spacer(1, 10))
        except Exception as e:
            # En caso de error al cargar la imagen, solo lo ignoramos
            pass
    
    # Comentarios
    elements.append(Paragraph("<b>Comentarios:</b>", styles["Heading3"]))
    elements.append(Paragraph(visit.comments, styles["Normal"]))
    elements.append(Spacer(1, 10))
    
    # Información de likes
    elements.append(Paragraph(f"<b>Me gusta:</b> {visit.likes_count}", styles["Normal"]))
    
    # Fecha de generación del PDF
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"Documento generado el {current_date}", styles["Italic"]))
    
    # Construir el PDF
    doc.build(elements)
    
    # Preparar la respuesta
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    
    # Configurar headers para descarga
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=visita_{visit_id}.pdf'
    
    return response