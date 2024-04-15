from flask import Flask, render_template
from conexionDB import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
#migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Reemplaza 'tu_clave_secreta_aqui' con una clave secreta única y segura


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    from views import views_blueprint
    app.register_blueprint(views_blueprint)

    app.run(debug=True)