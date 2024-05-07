from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager  # Importa LoginManager
from conexionDB import Config
from database import db, Usuario  # Asegúrate de importar Usuario si vas a usarlo en el cargador de usuario
from flask_migrate import Migrate
from views import login, get_user

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)  # Inicializa Flask-Login con la instancia de la app

@login_manager.user_loader  # Define el cargador de usuario
def load_user(user_id):
    return Usuario.query.get(int(user_id))

app.config['SESSION_PERMANENT'] = True
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.add_url_rule('/api/login', view_func=login, methods=['POST'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    from views import views_blueprint
    app.register_blueprint(views_blueprint)

    app.run(debug=True)
