from flask import Flask, render_template
from conexionDB import Config
from database import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Reemplaza 'tu_clave_secreta_aqui' con una clave secreta única y segura
app.config['SESSION_PERMANENT'] = True # si es true la sesion no expira
app.config['SESSION_REFRESH_EACH_REQUEST'] = True


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    from views import views_blueprint
    app.register_blueprint(views_blueprint)

    app.run(debug=True)