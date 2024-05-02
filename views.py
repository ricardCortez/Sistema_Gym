from flask import Blueprint, send_from_directory, render_template, request, redirect, url_for, session, jsonify
from database import db, Usuario
from utils import menu_manager

# Crear un Blueprint para las vistas
views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Ruta para el inicio de sesión
@views_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Usamos request.get_json() para manejar datos JSON
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
            return jsonify({"status": "success", "message": "Inicio de sesión exitoso"}), 200
        else:
            print("Inicio de sesión fallido")
            return jsonify({"status": "error", "message": "Usuario o contraseña incorrectos"}), 401

    # Si el método no es POST, simplemente devuelve el formulario de inicio de sesión
    return render_template('login.html')
@views_blueprint.route('/main')
def main():
    # Asume 'guest' si 'tipo_usuario' no está en la sesión
    user_type = session.get('tipo_usuario', 'guest')
    menu_options = menu_manager.get_menu(user_type)
    return render_template('dashboard.html', menu_options=menu_options)


@views_blueprint.route('/logout', methods=['POST'])
def logout():
    # Eliminar las variables de sesión
    #session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('tipo_usuario', None)
    # Redirigir al template principal
    return redirect('/')

@views_blueprint.route('/gestion-usuarios')
def gestion_usuarios():
    if 'tipo_usuario' not in session or session['tipo_usuario'] not in ['administrador']:
        return redirect(url_for('views.login'))
    return render_template('gestion_usuarios.html')

@views_blueprint.route('/sub1')
def subaction1():
    if 'tipo_usuario' not in session or session['tipo_usuario'] not in ['administrador']:
        return redirect(url_for('views.login'))
    return render_template('subaction1.html')

@views_blueprint.route('/sub2')
def subaction2():
    if 'tipo_usuario' not in session or session['tipo_usuario'] not in ['administrador']:
        return redirect(url_for('views.login'))
    return render_template('subaction2.html')

@views_blueprint.route('/reportes')
def reportes():
    if 'tipo_usuario' not in session or session['tipo_usuario'] not in ['administrador', 'dueño']:
        return redirect(url_for('views.reportes'))
    return render_template('main.html')

@views_blueprint.route('/promociones')
def promociones():
    if 'tipo_usuario' not in session or session['tipo_usuario'] not in ['administrador', 'counter', 'dueño']:
        return redirect(url_for('views.login'))
    return render_template('promociones.html')

@views_blueprint.route('/productos')
def productos():
    if 'tipo_usuario' not in session or session['tipo_usuario'] not in ['administrador', 'counter', 'dueño']:
        return redirect(url_for('views.login'))
    return render_template('productos.html')

@views_blueprint.route('/perfil')
def perfil():
    return render_template('perfil.html')