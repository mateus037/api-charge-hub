from flask import Blueprint, request, jsonify
from models import db
from models.location import Location
from models.charger import Charger

location_bp = Blueprint('location_bp', __name__)

@location_bp.route('/locations_with_chargers', methods=['GET'])
def get_all_locations_with_chargers():
    """
    Lista todas as localizações com seus carregadores
    ---
    tags:
      - Localizações
    responses:
      200:
        description: Lista de localizações com carregadores
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: Shopping Nova América
              address:
                type: string
                example: Av. Pastor Martin Luther King Jr., 126 - RJ
              chargers:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 5
                    status:
                      type: string
                      example: available
    """
    locations = Location.query.all()
    
    locations_data = []
    for loc in locations:
        chargers = Charger.query.filter_by(location_id=loc.id).all()
        locations_data.append({
            'id': loc.id,
            'name': loc.name,
            'address': loc.address,
            'chargers': [{'id': ch.id, 'status': ch.status} for ch in chargers]
        })
    
    return jsonify(locations_data)