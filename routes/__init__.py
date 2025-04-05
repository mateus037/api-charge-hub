from flask import Blueprint

# Importação dos Blueprints de cada módulo de rotas
from .user_routes import user_bp
from .location_routes import location_bp
from .charger_routes import charger_bp
from .appointment_routes import appointment_bp
# from .car_routes import car_bp

# Criar um Blueprint principal para agrupar todas as rotas (opcional)
api_bp = Blueprint('api_bp', __name__)

# Registrar todas as rotas no Blueprint principal
api_bp.register_blueprint(user_bp, url_prefix='/users')
api_bp.register_blueprint(location_bp, url_prefix='/locations')
api_bp.register_blueprint(charger_bp, url_prefix='/chargers')
api_bp.register_blueprint(appointment_bp, url_prefix='/appointments')
# api_bp.register_blueprint(car_bp, url_prefix='/cars')

# Lista de Blueprints para fácil registro no app principal
blueprints = [api_bp]
