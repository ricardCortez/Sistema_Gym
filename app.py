from flask import Flask, render_template
from flask_cors import CORS
from conexionDB import Config
from database import db
from flask_migrate import Migrate
from views import login, get_user

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Reemplaza 'tu_clave_secreta_aqui' con una clave secreta única y segura
app.config['SESSION_PERMANENT'] = True # si es true la sesion no expira
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.add_url_rule('/api/login', view_func=login, methods=['POST'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    from views import views_blueprint
    app.register_blueprint(views_blueprint)

    app.run(debug=True)