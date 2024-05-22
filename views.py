import os
import imutils
import cv2
from datetime import datetime, date
from flask import Blueprint, send_from_directory, render_template, request, redirect, url_for, session, jsonify
from database import db, Usuario, Socio, Entrenador, RegistroRostros, Asistencia
from face_detection import async_capture_faces, async_train_model, async_recognize_faces

# Crear un Blueprint para las vistas
views_blueprint = Blueprint('views', __name__)
# face_detection = f

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


@views_blueprint.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    file = request.files['file']
    face_id = request.form.get('face_id', 'default_id')
    async_capture_faces(file, face_id)
    return jsonify({"status": "success", "message": "Captura iniciada"}), 202


@views_blueprint.route('/api/train_model', methods=['POST'])
def train_model_route():
    try:
        async_train_model()
        return jsonify({"status": "success", "message": "Entrenamiento iniciado"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@views_blueprint.route('/api/recognize_faces', methods=['POST'])
def recognize_faces_route():
    try:
        async_recognize_faces()
        return jsonify({"status": "success", "message": "Reconocimiento iniciado"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500