# Configurtacion para la conexion a basa de datos
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/gymDB'  # Reemplaza con tu configuración de PostgreSQL
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:adminadmin@database-1.chceflvgkroz.us-east-2.rds.amazonaws.com/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False