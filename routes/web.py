from flask import Blueprint, render_template, abort

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    # Renderiza la Home con las secciones del embudo AIDA
    return render_template('index.html')

@web_bp.route('/nosotros')
def nosotros():
    return render_template('index.html', scroll_to='nosotros')

@web_bp.route('/servicios')
def servicios_hub():
    # Módulo Hub centralizado de servicios
    return render_template('servicios_hub.html')

@web_bp.route('/sesiones')
def sesiones():
    return render_template('paquetes/index.html', categories={})

@web_bp.route('/servicios/<slug>')
def servicio_individual(slug):
    # Lista de servicios válidos según documento técnico
    servicios_validos = [
        'produccion-audiovisual', 'video-corporativo', 'publicidad-comercial',
        'cobertura-eventos', 'streaming-profesional', 'documentales-reportajes',
        'fotografia-profesional', 'redes-sociales', 'drone-aereo'
    ]
    if slug not in servicios_validos:
        abort(404)
    # En producción aquí se consultaría a Sanity CMS o DB para traer los textos del servicio
    return render_template(f'servicios/detalle.html', servicio=slug)

@web_bp.route('/portafolio')
def portafolio():
    return render_template('index.html', scroll_to='portfolio')

@web_bp.route('/gracias')
def gracias():
    # Página post-conversión para evitar re-envíos de formulario (PRG Pattern)
    return render_template('gracias.html')