from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tipo_usuario = db.Column(db.String(20))  # Puede ser 'admin', 'dueño', 'counter', etc.

    def __init__(self, nombre, username, password, email, tipo_usuario):
        self.nombre = nombre
        self.username = username
        self.password = password
        self.email = email
        self.tipo_usuario = tipo_usuario

class Socio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))  # Nueva columna para los apellidos
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    fecha_registro = db.Column(db.Date, default=db.func.current_date())
    estado_membresia = db.Column(db.String(20))
    socio_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    codigo_unico = db.Column(db.String(36), unique=True)

    def __init__(self, nombre, apellidos, direccion, telefono, fecha_nacimiento, estado_membresia, socio_id, codigo_unico):
        self.nombre = nombre
        self.apellidos = apellidos  # Asegúrate de incluir los apellidos en el constructor
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.estado_membresia = estado_membresia
        self.socio_id = socio_id
        self.codigo_unico = codigo_unico

class Entrenador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    especialidad = db.Column(db.String(100))
    celular = db.Column(db.String(20))
    sexo = db.Column(db.String(10))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    codigo_unico = db.Column(db.String(36), unique=True)

    def __init__(self, nombre, apellidos, especialidad, celular, sexo, usuario_id, codigo_unico):
        self.nombre = nombre
        self.apellidos = apellidos
        self.especialidad = especialidad
        self.celular = celular
        self.sexo = sexo
        self.usuario_id = usuario_id
        self.codigo_unico = codigo_unico

class RegistroRostros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    socio_id = db.Column(db.Integer, db.ForeignKey('socio.id'), nullable=True)
    entrenador_id = db.Column(db.Integer, db.ForeignKey('entrenador.id'), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ruta = db.Column(db.String(200))

    socio = db.relationship('Socio', backref=db.backref('registros_rostros', lazy=True))
    entrenador = db.relationship('Entrenador', backref=db.backref('registros_rostros', lazy=True))

    def __init__(self, socio_id=None, entrenador_id=None, ruta=None):
        self.socio_id = socio_id
        self.entrenador_id = entrenador_id
        self.ruta = ruta

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
    socio_id = db.Column(db.Integer, db.ForeignKey('socio.id'), nullable=True)
    entrenador_id = db.Column(db.Integer, db.ForeignKey('entrenador.id'), nullable=True)

    socio = db.relationship('Socio', backref=db.backref('asistencias', lazy=True))
    entrenador = db.relationship('Entrenador', backref=db.backref('asistencias', lazy=True))

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer)
    categoria = db.Column(db.String(50))

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    fecha_venta = db.Column(db.Date)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    producto = db.relationship('Producto', backref=db.backref('ventas', lazy=True))
    socio_id = db.Column(db.Integer, db.ForeignKey('socio.id'))
    socio = db.relationship('Socio', backref=db.backref('ventas', lazy=True))
