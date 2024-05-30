import os
import imutils
import cv2
import threading
from datetime import datetime, date
from flask import Blueprint, send_from_directory, render_template, request, redirect, url_for, session, jsonify
from database import db, Usuario, Socio, Entrenador, RegistroRostros, Asistencia
from face_detection import async_recognize_faces, capture_faces, async_train_model, async_capture_faces

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


@views_blueprint.route('/prueba')
def prueba():
    return render_template('/prueba.html')


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


####################rutas para capturar - entrenar - reconocer rostros##########


@views_blueprint.route('/api/start_capture', methods=['POST'])
def start_capture():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file provided"}), 400
    file = request.files['file']
    face_id = request.form.get('face_id', 'default_id')
    current_count = int(request.form.get('current_count', 0))  # Recibe el contador actual desde el frontend
    file_stream = file.read()

    try:
        thread = async_capture_faces(file_stream, face_id, current_count, 300)
        thread.join()  # Esperar a que termine el hilo
        return jsonify({"status": "success", "message": f"Capture started. Images captured: {current_count + 1}"}), 202
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