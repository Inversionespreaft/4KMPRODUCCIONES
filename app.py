import re
import secrets
import string
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

from config import DevelopmentConfig
from models import db, Lead
from routes.web import web_bp
from routes.paquetes import paquetes_bp
from models import Code, Winner

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(DevelopmentConfig)

db.init_app(app)
mail = Mail(app)

# Registrar Blueprints
app.register_blueprint(web_bp)
app.register_blueprint(paquetes_bp)

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


def es_codigo_prueba(code):
    return code == '4KMTESTING'


def generar_codigo_unico(prefijo='CLT', longitud=6):
    alphabet = string.ascii_uppercase + string.digits
    while True:
        codigo = f"{prefijo}-{''.join(secrets.choice(alphabet) for _ in range(longitud))}"
        existing = Code.query.filter_by(code=codigo).first()
        if not existing:
            return codigo

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


@app.route('/api/validate_code', methods=['POST'])
def validate_code():
    code = request.form.get('code', '').strip().upper()
    if not code:
        return jsonify({'status': 'error', 'message': 'Código requerido.'}), 400
    if es_codigo_prueba(code):
        return jsonify({'status': 'ok', 'message': 'Código de pruebas válido.', 'package': 'testing'}), 200
    found = Code.query.filter_by(code=code).first()
    if not found:
        return jsonify({'status': 'invalid', 'message': 'Código inválido.'}), 404
    if found.used:
        return jsonify({'status': 'used', 'message': 'Código ya usado.'}), 400
    return jsonify({'status': 'ok', 'message': 'Código válido.', 'package': found.package}), 200


@app.route('/api/game_result', methods=['POST'])
def game_result():
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    telefono = request.form.get('telefono', '').strip()
    code = request.form.get('code', '').strip().upper()
    prize = request.form.get('prize', '').strip()
    package = request.form.get('package', '').strip()

    if not (nombre and prize):
        return jsonify({'status': 'error', 'message': 'Faltan datos obligatorios.'}), 400

    code_rec = None
    if code and not es_codigo_prueba(code):
        code_rec = Code.query.filter_by(code=code).first()
        if not code_rec:
            return jsonify({'status': 'error', 'message': 'Código inválido.'}), 404
        if code_rec.used:
            return jsonify({'status': 'error', 'message': 'Código ya usado.'}), 400

    try:
        winner = Winner(nombre=nombre, correo=correo or None, telefono=telefono or None, code=code or None, prize=prize, package=package or None)
        db.session.add(winner)
        if code_rec:
            code_rec.used = True
            db.session.add(code_rec)
        db.session.commit()
        return jsonify({'status': 'ok', 'message': 'Ganador registrado.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/admin/winners')
def admin_winners():
    winners = Winner.query.order_by(Winner.created_at.desc()).all()
    rows = ''.join([f"<tr><td>{w.id}</td><td>{w.nombre}</td><td>{w.correo or ''}</td><td>{w.telefono or ''}</td><td>{w.code or ''}</td><td>{w.prize}</td><td>{w.package or ''}</td><td>{w.created_at}</td></tr>" for w in winners])
    return f"<html><head><title>Winners</title></head><body><h2>Winners</h2><table border=1><tr><th>ID</th><th>Nombre</th><th>Correo</th><th>Teléfono</th><th>Código</th><th>Prize</th><th>Package</th><th>Fecha</th></tr>{rows}</table></body></html>"


@app.route('/admin/create_code', methods=['POST'])
def admin_create_code():
    # Simple admin helper to create single-use codes (use protected in production)
    code = request.form.get('code', '').strip().upper()
    package = request.form.get('package', '').strip()
    assigned = request.form.get('assigned_to', '').strip()
    if not code:
        return jsonify({'status': 'error', 'message': 'Código requerido.'}), 400
    existing = Code.query.filter_by(code=code).first()
    if existing:
        return jsonify({'status': 'error', 'message': 'Código ya existe.'}), 400
    try:
        c = Code(code=code, package=package or None, assigned_to=assigned or None)
        db.session.add(c)
        db.session.commit()
        return jsonify({'status': 'ok', 'message': 'Código creado.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/admin/generate_client_codes', methods=['POST'])
def generate_client_codes():
    quantity = request.form.get('quantity', '1').strip()
    package = request.form.get('package', '').strip()
    assigned = request.form.get('assigned_to', '').strip()

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Cantidad inválida.'}), 400

    if quantity < 1 or quantity > 100:
        return jsonify({'status': 'error', 'message': 'La cantidad debe estar entre 1 y 100.'}), 400

    generated = []
    try:
        for _ in range(quantity):
            codigo = generar_codigo_unico(prefijo='CLT', longitud=6)
            c = Code(code=codigo, package=package or None, assigned_to=assigned or None)
            db.session.add(c)
            generated.append(codigo)
        db.session.commit()
        return jsonify({'status': 'ok', 'message': 'Códigos generados.', 'codes': generated}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

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