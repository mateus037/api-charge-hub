from flask import Blueprint, request, jsonify
from models import db
from models.charger import Charger

charger_bp = Blueprint('charger_bp', __name__)

@charger_bp.route('/', methods=['GET'])
def get_chargers():
    """
    Lista todos os carregadores disponíveis
    ---
    tags:
      - Carregadores
    responses:
      200:
        description: Lista de carregadores cadastrados
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              location_id:
                type: integer
                example: 3
              status:
                type: string
                example: available
    """
    chargers = Charger.query.all()
    return jsonify([{'id': ch.id, 'location_id': ch.location_id, 'status': ch.status} for ch in chargers])

@charger_bp.route('/', methods=['POST'])
def create_charger():
    """
    Cria um novo carregador em uma localização existente
    ---
    tags:
      - Carregadores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - location_id
          properties:
            location_id:
              type: integer
              example: 3
              description: ID da localização onde o carregador será cadastrado
            status:
              type: string
              example: available
              description: Status do carregador (opcional, padrão 'available')
    responses:
      201:
        description: Carregador criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: Carregador criado com sucesso!
      400:
        description: Erro na requisição (dados inválidos)
        schema:
          type: object
          properties:
            error:
              type: string
              example: O campo location_id é obrigatório
    """
    data = request.json
    new_charger = Charger(
        location_id=data['location_id'],
        status=data.get('status', 'available')
    )
    db.session.add(new_charger)
    db.session.commit()
    return jsonify({'message': 'Carregador criado com sucesso!'}), 201
