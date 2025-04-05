from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config.config import Config
from models import db
from routes import blueprints
from models.location import Location
from models.charger import Charger

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

locations_data = [
    {"name": "Shopping Center", "address": "Av. Principal, 123"},
    {"name": "Estação Central", "address": "Rua da Estação, 45"},
    {"name": "Supermercado X", "address": "Av. Comercial, 789"},
    {"name": "Bodytech", "address": "Av. Dom Hélder Câmara, 5474 - Cachambi, Rio de Janeiro - RJ, 20771-004"},
    {"name": "Shopping Nova America", "address": "Av. Pastor Martin Luther King Jr., 126 - Del Castilho, Rio de Janeiro - RJ, 20765-000"},
    {"name": "Super Mercados Guanabara", "address": "Rua da Estação. RJ, 45"},
    {"name": "Supermercado A", "address": "Av. Comercial, 800"},
    {"name": "Estacionamento x", "address": "Av. Dom Hélder Câmara, 0001 - Cachambi, Rio de Janeiro - RJ, 20371-004"},
]

chargers_data = [
    {"location_id": 1, "status": "available"},
    {"location_id": 2, "status": "unavailable"},
    {"location_id": 3, "status": "maintenance"},
    {"location_id": 4, "status": "available"},
    {"location_id": 5, "status": "available"},
    {"location_id": 6, "status": "available"},
    {"location_id": 7, "status": "maintenance"},
    {"location_id": 8, "status": "available"},
]

def seed_database():
    """ Insere os dados iniciais no banco apenas se ainda não existirem """
    if not Location.query.first():
        print("📌 Populando banco de dados com dados iniciais...")
        
        for loc in locations_data:
            location = Location(**loc)
            db.session.add(location)
        
        db.session.commit()

        for charger in chargers_data:
            charger_instance = Charger(**charger)
            db.session.add(charger_instance)

        db.session.commit()

        print("✅ Dados iniciais inseridos com sucesso!")

for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

@app.route('/')
def home():
    return "Olá, Flask!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True)