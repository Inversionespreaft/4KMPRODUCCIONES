import os
import re
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración básica y de seguridad
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '4KM_Secret_Ultra_Premium_Key_2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads_4km.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de Mail (Ajustar con credenciales reales en producción)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'contacto@4kmproducciones.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'tu_password_seguro')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'contacto@4kmproducciones.com')

db = SQLAlchemy(app)
mail = Mail(app)

# Modelo de Base de Datos para Leads
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    servicio = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())

# Inicializar Base de Datos dentro del contexto de la App
with app.app_context():
    db.create_all()

# Helper de validación básica Anti-Spam
def es_valido(texto):
    # Bloquear patrones comunes de bots de spam
    patrones_spam = [r"http://", r"https://", r"www\.", r"\[url=\]", r"href="]
    for patron in patrones_spam:
        if re.search(patron, texto, re.IGNORECASE):
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    telefono = request.form.get('telefono', '').strip()
    servicio = request.form.get('servicio', '').strip()
    mensaje = request.form.get('mensaje', '').strip()
    honeypot = request.form.get('website', '').strip() # Campo oculto anti-bots

    # 1. Protección Anti-Spam Honeypot
    if honeypot:
        return jsonify({"status": "error", "message": "Bot detectado."}), 400

    # 2. Validaciones de servidor
    if not (nombre and correo and telefono and servicio and mensaje):
        return jsonify({"status": "error", "message": "Todos los campos son obligatorios."}), 400

    if not es_valido(nombre) or not es_valido(mensaje):
        return jsonify({"status": "error", "message": "Contenido sospechoso detectado."}), 400

    try:
        # 3. Guardar en Base de Datos
        nuevo_lead = Lead(nombre=nombre, correo=correo, telefono=telefono, servicio=servicio, mensaje=mensaje)
        db.session.add(nuevo_lead)
        db.session.commit()

        # 4. Envío de Correo de Notificación (Asíncrono en entornos robustos)
        msg = Message(
            subject=f"Nuevo Lead 4KM: {servicio} - {nombre}",
            recipients=[app.config['MAIL_USERNAME']],
            body=f"Nombre: {nombre}\nCorreo: {correo}\nTeléfono: {telefono}\nServicio: {servicio}\nMensaje: {mensaje}"
        )
        # Descomentar en entorno configurado:
        # mail.send(msg)

        return jsonify({"status": "success", "message": "Propuesta enviada con éxito. Nos comunicaremos de inmediato."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Error interno en el servidor: {str(e)}"}), 500

# Panel Básico Administrativo Protegido (Hardcoded para fines demostrativos)
@app.route('/admin/dashboard')
def admin_dashboard():
    # En producción implementar flask_login o decoradores JWT
    leads = Lead.query.order_by(Lead.fecha.desc()).all()
    return f"""
    <html>
        <head>
            <title>4KM Dashboard</title>
            <style>
                body {{ font-family: sans-serif; background: #0B0B0B; color: #FFF; padding: 40px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #D4AF37; padding: 12px; text-align: left; }}
                th {{ background: #121212; color: #D4AF37; }}
                tr:nth-child(even) {{ background: #1a1a1a; }}
            </style>
        </head>
        <body>
            <h2>Panel de Leads - 4KM Producciones</h2>
            <table>
                <tr><th>ID</th><th>Nombre</th><th>Correo</th><th>Teléfono</th><th>Servicio</th><th>Mensaje</th><th>Fecha</th></tr>
                {"".join([f"<tr><td>{l.id}</td><td>{l.nombre}</td><td>{l.correo}</td><td>{l.telefono}</td><td>{l.servicio}</td><td>{l.mensaje}</td><td>{l.fecha}</td></tr>" for l in leads])}
            </table>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)