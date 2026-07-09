from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    servicio = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    duracion = db.Column(db.String(80), nullable=False)
    incluye = db.Column(db.Text, nullable=False)
    lugar = db.Column(db.String(120), nullable=False)
    tiempo_entrega = db.Column(db.String(80), nullable=False)
    imagen_principal = db.Column(db.String(255), nullable=True)
    imagenes = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(20), default='publicado')
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


class Code(db.Model):
    __tablename__ = 'codes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(120), unique=True, nullable=False)
    assigned_to = db.Column(db.String(200), nullable=True)
    package = db.Column(db.String(140), nullable=True)
    used = db.Column(db.Boolean, default=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


class Winner(db.Model):
    __tablename__ = 'winners'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(40), nullable=True)
    code = db.Column(db.String(120), nullable=True)
    prize = db.Column(db.String(255), nullable=False)
    package = db.Column(db.String(140), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
