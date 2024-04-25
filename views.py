from flask import Blueprint, render_template, request, redirect, url_for, session
from database import db, Usuario

# Crear un Blueprint para las vistas
views_blueprint = Blueprint('views', __name__)

# Ruta para el inicio de sesión
@views_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print("Valor de Username:", username)  # Agrega este print para ver el valor de username
        print("Valor de Password:", password)  # Agrega este print para ver el valor de password

        # Busca el usuario en la base de datos
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.password == password:  # Agrega este print para verificar si la validación de contraseña es correcta
            session['id'] = usuario.id # Guarda el id de usuario en la sesión
            # Usuario y contraseña válidos, inicia sesión
            session['username'] = username  # Guarda el nombre de usuario en la sesión
            session['nombre'] = usuario.nombre # guarda el nombre
            session['tipo_usuario'] = usuario.tipo_usuario # Verifica y guarda el tipo de perfil en la sesion
            print("Id del usuario: ", usuario.id)
            print("Inicio de sesión exitoso")  # Agrega este print para confirmar el inicio de sesión exitoso
            print("Tipo de usuario: ", usuario.tipo_usuario)
            #return redirect(url_for('views.login'))
            return 'Inicio de sesión exitoso'
        else:
            error = 'Usuario o contraseña incorrectos. Por favor, intenta nuevamente.'
            print("Inicio de sesión fallido")  # Agrega este print para confirmar el inicio de sesión fallido
            #return render_template('login.html', error=error)
            return 'Usuario o contraseña incorrectos. Por favor, intenta nuevamente.'

    return render_template('login.html')
@views_blueprint.route('/main')
def main():
    return render_template('dashboard.html')


@views_blueprint.route('/logout', methods=['POST'])
def logout():
    # Eliminar las variables de sesión
    #session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('tipo_usuario', None)
    # Redirigir al template principal
    return redirect('/')