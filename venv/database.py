from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Socio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    fecha_registro = db.Column(db.Date, default=db.func.current_date())
    estado_membresia = db.Column(db.String(20))
    foto_ruta = db.Column(db.String(200))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Membresia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    precio = db.Column(db.Numeric(10, 2))
    duracion_dias = db.Column(db.Integer)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado_pago = db.Column(db.String(20))
    socio_id = db.Column(db.Integer, db.ForeignKey('socio.id'))
    socio = db.relationship('Socio', backref=db.backref('membresias', lazy=True))

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Numeric(10, 2))
    fecha_pago = db.Column(db.Date)
    tipo_pago = db.Column(db.String(50))
    membresia_id = db.Column(db.Integer, db.ForeignKey('membresia.id'))
    membresia = db.relationship('Membresia', backref=db.backref('pagos', lazy=True))

class Entrenador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    especialidad = db.Column(db.String(100))
    celular = db.Column(db.String(20))
    sexo = db.Column(db.String(10))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Entrenamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    socio_id = db.Column(db.Integer, db.ForeignKey('socio.id'))
    socio = db.relationship('Socio', backref=db.backref('entrenamientos', lazy=True))
    entrenador_id = db.Column(db.Integer, db.ForeignKey('entrenador.id'))
    entrenador = db.relationship('Entrenador', backref=db.backref('entrenamientos', lazy=True))

class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    hora_entrada = db.Column(db.Time)
    hora_salida = db.Column(db.Time)
    tipo_usuario = db.Column(db.String(10))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tipo_usuario = db.Column(db.String(20))  # Puede ser 'admin', 'socio', 'entrenador', etc.
