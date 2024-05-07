from flask import Blueprint, send_from_directory, render_template, request, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from database import db, Usuario
from utils import menu_manager

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


@views_blueprint.route('/main')
def main():
    user_type = session.get('tipo_usuario')
    menu_options = menu_manager.get_menu(user_type)
    return render_template('dashboard.html', menu_options=menu_options)


@views_blueprint.route('/logout', methods=['POST'])
def logout():
    # Eliminar las variables de sesión
    session.pop('id', None)
    session.pop('username', None)
    session.pop('tipo_usuario', None)
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

