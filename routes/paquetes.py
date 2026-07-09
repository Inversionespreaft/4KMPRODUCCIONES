import re
from flask import Blueprint, render_template, abort

paquetes_bp = Blueprint('paquetes', __name__)


def _slugify(text):
    text = text.lower()
    text = re.sub(r'[áàäâãå]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöôõ]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

CATEGORY_DATA = {
    'parejas': {
        'title': 'Parejas',
        'subtitle': 'Sesiones de pareja con atmósfera cinematográfica',
        'teaser': 'Sesiones románticas en exteriores y estudio con entrega digital y soporte impreso.',
        'whatsapp': '51924130007',
        'packages': [
            {
                'name': 'Estándar',
                'price': 'S/300',
                'description': 'Cobertura básica para parejas con 1 hora de sesión y entrega ágil.',
                'features': [
                    '1 hora de sesión',
                    '10 fotografías digitales',
                    '2 impresiones 10×15',
                    '1 collage digital',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Parejas+Est%C3%A1ndar'
            },
            {
                'name': 'Avanzado',
                'price': 'S/420',
                'description': 'Sesión ampliada con más entregables y opciones de look adicionales.',
                'features': [
                    '1.5 horas de sesión',
                    '15 fotografías digitales',
                    '4 impresiones 10×15',
                    '1 cuadro 15×20',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Parejas+Avanzado'
            },
            {
                'name': 'Premium',
                'price': 'S/550',
                'description': 'Experiencia completa con styling, locación premium y entrega ampliada.',
                'features': [
                    '2 horas de sesión',
                    '25 fotografías digitales',
                    '6 impresiones 10×15',
                    '2 collages digitales',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Parejas+Premium'
            }
        ]
    },
    'familiar': {
        'title': 'Familiar',
        'subtitle': 'Sesiones familiares para capturar emociones reales y recuerdos duraderos.',
        'teaser': 'Cobertura para familias en exteriores o estudio con fotografías de alto impacto.',
        'whatsapp': '51924130007',
        'packages': [
            {
                'name': 'Familiar Básico',
                'price': 'S/320',
                'description': 'Sesión ideal para familias pequeñas con entrega digital profesional.',
                'features': [
                    '1 hora de sesión',
                    '12 fotografías digitales',
                    '1 collage digital',
                    '2 fotos impresas 10×15',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Familiar+B%C3%A1sico'
            },
            {
                'name': 'Familiar Plus',
                'price': 'S/450',
                'description': 'Más tiempo y fotografías para familias grandes o multi-generacionales.',
                'features': [
                    '1.5 horas de sesión',
                    '18 fotografías digitales',
                    '4 fotos impresas 10×15',
                    '1 álbum digital',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Familiar+Plus'
            },
            {
                'name': 'Familiar Premium',
                'price': 'S/600',
                'description': 'Producción completa con styling y entrega para impresiones y redes.',
                'features': [
                    '2 horas de sesión',
                    '25 fotografías digitales',
                    '6 impresiones 10×15',
                    '1 galería online privada',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Familiar+Premium'
            }
        ]
    },
    'quince-anos': {
        'title': 'Quince Años',
        'subtitle': 'Sesiones de 15 años con estilo cinematográfico y presencia en redes.',
        'teaser': 'Cobertura de quinceañeras con recuerdos elegantes y contenido para redes sociales.',
        'whatsapp': '51924130007',
        'packages': [
            {
                'name': 'Sweet 15',
                'price': 'S/550',
                'description': 'Sesión preparada para looks formales y detalles de presentación.',
                'features': [
                    '1.5 horas de sesión',
                    '20 fotografías digitales',
                    '3 impresiones 10×15',
                    '1 mini video teaser',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Quince+A%C3%B1os+Sweet+15'
            },
            {
                'name': '15 Premium',
                'price': 'S/720',
                'description': 'Sesión extendida con cambio de looks y entrega premium para álbum.',
                'features': [
                    '2.5 horas de sesión',
                    '30 fotografías digitales',
                    '5 impresiones 10×15',
                    '1 álbum digital',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Quince+A%C3%B1os+Premium'
            }
        ]
    },
    'graduacion': {
        'title': 'Graduación',
        'subtitle': 'Cobertura de graduaciones con narrativa visual memorable.',
        'teaser': 'Paquetes para sesión de toga, ceremonia y video de celebración.',
        'whatsapp': '51924130007',
        'packages': [
            {
                'name': 'Graduación Fast',
                'price': 'S/270',
                'description': 'Sesión breve para fotos de toga y recuerdos inmediatos.',
                'features': [
                    '45 minutos de sesión',
                    '12 fotografías digitales',
                    '1 collage digital',
                    'Entrega en 5 días',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Graduaci%C3%B3n+Fast'
            },
            {
                'name': 'Graduación Plus',
                'price': 'S/420',
                'description': 'Sesión con ceremonias y tomas al aire libre para un recuerdo completo.',
                'features': [
                    '1.5 horas de sesión',
                    '20 fotografías digitales',
                    '2 impresiones 10×15',
                    '1 video short clip',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Graduaci%C3%B3n+Plus'
            }
        ]
    },
    'bodas': {
        'title': 'Bodas',
        'subtitle': 'Producción audiovisual para bodas con estilo documental y cinematográfico.',
        'teaser': 'Cobertura de bodas con fotos, video y recuerdos emocionales.',
        'whatsapp': '51924130007',
        'packages': [
            {
                'name': 'Boda Esencial',
                'price': 'S/1200',
                'description': 'Cobertura de ceremonia y sesión romántica con entrega digital.',
                'features': [
                    '4 horas de cobertura',
                    '80 fotografías digitales',
                    '1 video highlight',
                    'Galería online privada',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Bodas+Esencial'
            },
            {
                'name': 'Boda Premium',
                'price': 'S/2100',
                'description': 'Cobertura completa del día, video cinematográfico y sesión de preboda.',
                'features': [
                    '8 horas de cobertura',
                    '120 fotografías digitales',
                    'Video highlight + teaser',
                    '2 cámaras y dron',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Bodas+Premium'
            }
        ]
    },
    'linkedin': {
        'title': 'LinkedIn',
        'subtitle': 'Contenido profesional para LinkedIn, personal branding y posicionamiento ejecutivo.',
        'teaser': 'Sesiones rápidas para retratos ejecutivos y videos corporativos personales.',
        'whatsapp': '51924130007',
        'packages': [
            {
                'name': 'Perfil Ejecutivo',
                'price': 'S/280',
                'description': 'Retratos profesionales y fotos para uso en LinkedIn y CV.',
                'features': [
                    '30 minutos de sesión',
                    '10 fotografías retocadas',
                    '2 fondos distintos',
                    'Entrega digital rápida',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+LinkedIn+Perfil+Ejecutivo'
            },
            {
                'name': 'Branding Corporativo',
                'price': 'S/520',
                'description': 'Video corto y retratos para personal branding con estilo premium.',
                'features': [
                    '1 hora de sesión',
                    '10 fotografías profesionales',
                    '1 video corto de presentación',
                    'Asesoría de estilo',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+LinkedIn+Branding+Corporativo'
            }
        ]
    },
    'embarazo': {
        'title': 'Embarazo',
        'subtitle': 'Sesiones de maternidad con sensibilidad y fotografía de autor.',
        'teaser': 'Captura el momento más especial antes de la llegada con estilo cuidado.',
        'whatsapp': '51924130007',
        'packages': [
            {
                'name': 'Maternidad Básica',
                'price': 'S/340',
                'description': 'Sesión elegante para la futura mamá con 1 local y entrega digital.',
                'features': [
                    '1 hora de sesión',
                    '12 fotografías digitales',
                    '1 impresión 10×15',
                    '1 collage digital',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Embarazo+B%C3%A1sico'
            },
            {
                'name': 'Maternidad Premium',
                'price': 'S/520',
                'description': 'Sesión taller con styling, accesorios y fotos de pareja.',
                'features': [
                    '2 horas de sesión',
                    '20 fotografías digitales',
                    '3 impresiones 10×15',
                    '1 álbum digital',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Embarazo+Premium'
            }
        ]
    },
    'tematicas': {
        'title': 'Temáticas',
        'subtitle': 'Sesiones creativas temáticas para campañas, cumpleaños y eventos especiales.',
        'teaser': 'Producciones con escenarios y concepto visual para contenidos empaquetados.',
        'whatsapp': '51924130007',
        'packages': [
            {
                'name': 'Concepto Exprés',
                'price': 'S/390',
                'description': 'Sesión temática rápida con dirección de arte ligera.',
                'features': [
                    '1 hora de sesión',
                    '15 fotografías digitales',
                    '1 video short',
                    'Asesoría de concepto',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Tem%C3%A1ticas+Expr%C3%A9s'
            },
            {
                'name': 'Temática Premium',
                'price': 'S/760',
                'description': 'Producción temática con atrezzo, locación y contenido para redes.',
                'features': [
                    '3 horas de producción',
                    '30 fotografías digitales',
                    '2 videos cortos',
                    'Dirección creativa completa',
                ],
                'whatsapp_message': 'Hola+4KM,+quiero+informaci%C3%B3n+sobre+el+paquete+Tem%C3%A1ticas+Premium'
            }
        ]
    }
}

for category in CATEGORY_DATA.values():
    for package in category['packages']:
        package['slug'] = _slugify(package['name'])


def _render_category(slug):
    category = CATEGORY_DATA.get(slug)
    if not category:
        abort(404)
    return render_template('paquetes/category.html', category=category, slug=slug)


def _find_package(category_slug, package_slug):
    category = CATEGORY_DATA.get(category_slug)
    if not category:
        return None, None
    for package in category['packages']:
        if package.get('slug') == package_slug:
            return category, package
    return category, None


@paquetes_bp.route('/paquetes')
def paquetes_index():
    return render_template('paquetes/index.html', categories=CATEGORY_DATA)


@paquetes_bp.route('/paquetes/<category_slug>')
def category_page(category_slug):
    return _render_category(category_slug)


@paquetes_bp.route('/paquetes/<category_slug>/<package_slug>')
def package_detail(category_slug, package_slug):
    category, package = _find_package(category_slug, package_slug)
    if not category or not package:
        abort(404)
    return render_template('paquetes/detail.html', category=category, package=package, category_slug=category_slug)


@paquetes_bp.route('/parejas')
def parejas():
    return _render_category('parejas')


@paquetes_bp.route('/familiar')
def familiar():
    return _render_category('familiar')


@paquetes_bp.route('/quince-anos')
def quince_anos():
    return _render_category('quince-anos')


@paquetes_bp.route('/graduacion')
def graduacion():
    return _render_category('graduacion')


@paquetes_bp.route('/bodas')
def bodas():
    return _render_category('bodas')


@paquetes_bp.route('/linkedin')
def linkedin():
    return _render_category('linkedin')


@paquetes_bp.route('/embarazo')
def embarazo():
    return _render_category('embarazo')


@paquetes_bp.route('/tematicas')
def tematicas():
    return _render_category('tematicas')
