
import threading
from flask import Blueprint, send_from_directory, request, session, jsonify
from database import db, Usuario, Socio, Entrenador, RegistroRostros, Asistencia
from face_detection import async_recognize_faces, capture_faces, async_train_model
# Crear un Blueprint para las vistas
views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Ruta para el inicio de sesión
@views_blueprint.route('/', methods=['GET', 'POST'])
def login():
    data = request.get_json()  # Obtener los datos enviados en formato JSON
    username = data['username']
    password = data['password']
    print("Valor de Username:", username)
    print("Valor de Password:", password)

    # Busca el usuario en la base de datos
    usuario = Usuario.query.filter_by(username=username).first()

    if usuario and usuario.password == password:
        session['id'] = usuario.id
        session['username'] = username
        session['nombre'] = usuario.nombre
        session['tipo_usuario'] = usuario.tipo_usuario
        print("Id del usuario: ", usuario.id)
        print("Inicio de sesión exitoso")
        print("Tipo de usuario: ", usuario.tipo_usuario)
        return jsonify({
            "status": "success",
            "user": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "tipo_usuario": usuario.tipo_usuario
            }
        }), 200
    else:
        print("Inicio de sesión fallido")
        return jsonify({"status": "error", "message": "Usuario o contraseña incorrectos"}), 401


# @views_blueprint.route('/prueba')
# def prueba():
#     return render_template('/prueba.html')


@views_blueprint.route('/logout', methods=['POST'])
def logout():
    # Eliminar las variables de sesión
    session.pop('id', None)
    session.pop('username', None)
    session.pop('tipo_usuario', None)
    print("Sesion cerrada exitosa")
    return jsonify({'status': 'success', 'message': 'Logged out successfully'}), 200


@views_blueprint.route('/api/get_user')
def get_user():
    user_id = session.get('id')
    if user_id is None:
        return jsonify({"message": "No user logged in"}), 401  # Asegúrate de retornar 401 si no hay usuario

    # asumimos que 'Usuario' es tu modelo y 'user_id' es válido
    usuario = Usuario.query.get(user_id)
    if usuario:
        return jsonify({
            "status": "success",
            "user": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "tipo_usuario": usuario.tipo_usuario,
                "email": usuario.email
            }
        }), 200

    else:
        return jsonify({"message": "User not found"}), 404


@views_blueprint.route('/api/update_user', methods=['POST'])
def update_user():
    data = request.json
    user_id = data.get('id')  # Asumiendo que el ID del usuario viene en los datos JSON
    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"error": "User not found"}), 404

    try:
        if 'nombre' in data:
            usuario.nombre = data['nombre']
        if 'tipo_usuario' in data:
            usuario.tipo_usuario = data['tipo_usuario']
        if 'email' in data:
            usuario.email = data['email']

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@views_blueprint.route('/api/generate_unique_code', methods=['GET'])
def generate_unique_code():
    last_socio = Socio.query.order_by(Socio.id.desc()).first()
    if last_socio and last_socio.codigo_unico:
        new_code = int(last_socio.codigo_unico) + 1
    else:
        new_code = 1000
    return jsonify({"codigo_unico": str(new_code).zfill(4)})


@views_blueprint.route('/api/save_socio_data', methods=['POST'])
def save_socio_data():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    # Asegúrate de que todos los campos necesarios están presentes
    required_fields = ['nombre', 'apellidos', 'direccion', 'telefono', 'fecha_nacimiento', 'fecha_registro', 'estado_membresia', 'codigo_unico']
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing one or more required fields"}), 400

    # Crea una instancia del modelo Socio
    nuevo_socio = Socio(
        nombre=data['nombre'],
        apellidos=data['apellidos'],
        direccion=data['direccion'],
        telefono=data['telefono'],
        fecha_nacimiento=data['fecha_nacimiento'],
        fecha_registro=data['fecha_registro'],
        estado_membresia=data['estado_membresia'],
        codigo_unico=data['codigo_unico']
    )

    try:
        db.session.add(nuevo_socio)
        db.session.commit()
        return jsonify({"status": "success", "message": "Datos del socio guardados correctamente."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# rutas para capturar - entrenar - reconocer rostros##########


@views_blueprint.route('/api/start_capture', methods=['POST'])
def start_capture():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file provided"}), 400

    file = request.files['file']
    codigo_unico = request.form.get('codigo_unico', 'default_id')  # Usar codigo_unico en lugar de face_id
    current_count = int(request.form.get('current_count', 0))  # Recibe el contador actual desde el frontend
    file_stream = file.read()

    try:
        count = capture_faces(file_stream, codigo_unico, current_count)  # Llamar directamente a capture_faces para simplicidad
        captured = count > current_count  # Verificar si se capturó alguna imagen
        return jsonify({"status": "success", "message": f"Capture started. Images captured: {count - current_count}", "captured": captured, "new_count": count}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@views_blueprint.route('/api/train_model', methods=['POST'])
def train_model_route():
    try:
        async_train_model()
        return jsonify({"status": "success", "message": "Entrenamiento iniciado"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


validation_status = {
    "status": "pending"
}
status_lock = threading.Lock()


@views_blueprint.route('/api/recognize_faces', methods=['POST'])
def recognize_faces_route():
    global validation_status
    try:
        with status_lock:
            validation_status["status"] = "pending"
        async_recognize_faces()
        return jsonify({"status": "success", "message": "Reconocimiento iniciado"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@views_blueprint.route('/api/face_validated', methods=['POST'])
def face_validated_route():
    global validation_status
    try:
        with status_lock:
            validation_status["status"] = "validated"
        return jsonify({"status": "success", "message": "Usuario validado"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@views_blueprint.route('/api/check_validation_status', methods=['GET'])
def check_validation_status():
    global validation_status
    with status_lock:
        return jsonify({"status": validation_status["status"]})