import os

import cv2
from flask import Blueprint, send_from_directory, render_template, request, redirect, url_for, session, jsonify
#from flask_login import login_required, current_user
from database import db, Usuario
from face_detection import FaceDetector

# from views import views_blueprint

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

    return render_template('prueba.html')


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


face_detector = FaceDetector()


@views_blueprint.route('/train', methods=['POST'])
def train():
    # Supón que recibes imágenes etiquetadas para el entrenamiento
    images = [cv2.imread(file) for file in os.listdir('path_to_training_images')]
    labels = [int(label) for label in open('path_to_labels_file').read().split()]
    face_detector.train_recognizer(images, labels)
    return jsonify({'message': 'Model trained successfully'})


@views_blueprint.route('/detect_faces', methods=['POST'])
def detect_faces():
    file = request.files['image']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    img_bytes = file.read()
    faces_detected = face_detector.process_image(img_bytes)

    if not faces_detected:
        return jsonify({'message': 'No faces detected'}), 200

    # Construye una respuesta asegurando que todo es serializable y apropiado para JSON
    faces_info = [
        {'face_id': i, 'label': str(face['label']), 'confidence': float(face['confidence']), 'box': face['box']}
        for i, face in enumerate(faces_detected)
    ]

    return jsonify({'message': f'{len(faces_detected)} faces detected', 'faces': faces_info}), 200
