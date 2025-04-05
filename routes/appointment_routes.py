from flask import Blueprint, request, jsonify
from models import db
from models.appointment import Appointment
from models.user import User
from models.charger import Charger
from models.location import Location
from utils.datetime_utils import parse_iso_datetime

appointment_bp = Blueprint('appointment_bp', __name__)

@appointment_bp.route("/", methods=["POST"])
def create_appointment():
    """
    Cria um novo agendamento
    ---
    tags:
      - Agendamentos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - local
            - email
            - start_time
            - end_time
          properties:
            local:
              type: string
              example: Estacionamento x
              description: Nome do local onde será feito o agendamento
            email:
              type: string
              example: joao@email.com
              description: Email do usuário que está agendando
            start_time:
              type: string
              format: date-time
              example: 2025-04-03T12:00
              description: Início do agendamento (formato ISO 8601)
            end_time:
              type: string
              format: date-time
              example: 2025-04-03T16:00
              description: Fim do agendamento (formato ISO 8601)
    responses:
      201:
        description: Agendamento criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: Agendamento criado com sucesso!
            appointment:
              type: object
              properties:
                id:
                  type: integer
                  example: 10
                user:
                  type: string
                  example: joao@email.com
                local:
                  type: string
                  example: Estacionamento x
                charger_id:
                  type: integer
                  example: 3
                start_time:
                  type: string
                  format: date-time
                  example: 2025-04-03T12:00 
                end_time:
                  type: string
                  format: date-time
                  example: 2025-04-03T16:00
                status:
                  type: string
                  example: confirmed
      400:
        description: Erro de validação (campos obrigatórios ou formato incorreto)
        schema:
          type: object
          properties:
            error:
              type: string
              example: Campo obrigatório 'email' não informado
      404:
        description: Usuário, local ou carregador não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Local não encontrado
      500:
        description: Erro interno ao criar o agendamento
        schema:
          type: object
          properties:
            error:
              type: string
              example: Erro inesperado ao processar a requisição
    """
    try:
        data = request.json

        # Validar se todos os campos obrigatórios foram enviados
        required_fields = ["local", "email", "start_time", "end_time"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Campo obrigatório '{field}' não informado"}), 400

        # Buscar o usuário pelo email
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        # Buscar o local pelo nome
        location = Location.query.filter_by(name=data["local"]).first()
        if not location:
            return jsonify({"error": "Local não encontrado"}), 404

        # Buscar um carregador (charger) associado a esse local
        charger = Charger.query.filter_by(location_id=location.id).first()
        if not charger:
            return jsonify({"error": "Nenhum carregador disponível neste local"}), 404

        # Converter datas
        try:
            start_time = parse_iso_datetime(data["start_time"])
            end_time = parse_iso_datetime(data["end_time"])
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)"}), 400

        # Verificar se o horário de término é depois do início
        if end_time <= start_time:
            return jsonify({"error": "O horário de término deve ser maior que o de início"}), 400

        # Criar o agendamento
        new_appointment = Appointment(
            user_id=user.id,
            charger_id=charger.id,
            start_time=start_time,
            end_time=end_time,
            status="confirmed"
        )

        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({
            "message": "Agendamento criado com sucesso!",
            "appointment": {
                "id": new_appointment.id,
                "user": user.email,
                "local": location.name,
                "charger_id": charger.id,
                "start_time": new_appointment.start_time.isoformat(),
                "end_time": new_appointment.end_time.isoformat(),
                "status": new_appointment.status
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@appointment_bp.route("/<int:user_id>", methods=["GET"])
def get_user_appointments(user_id):
    """
    Retorna todos os agendamentos de um usuário
    ---
    tags:
      - Agendamentos
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário
        example: 2
    responses:
      200:
        description: Lista de agendamentos do usuário
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 12
              local:
                type: string
                example: Estacionamento x
              endereco:
                type: string
                example: Av. Principal, 123
              start_time:
                type: string
                format: date-time
                example: 2025-04-03T15:00:00
              end_time:
                type: string
                format: date-time
                example: 2025-04-03T17:00:00
              status:
                type: string
                example: confirmado
      404:
        description: Usuário não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Usuário não encontrado
      500:
        description: Erro interno no servidor
        schema:
          type: object
          properties:
            error:
              type: string
              example: Ocorreu um erro ao buscar os agendamentos
    """
    try:
        # Verifica se o usuário existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        # Busca os agendamentos do usuário
        appointments = Appointment.query.filter_by(user_id=user_id).all()

        # Se não houver agendamentos, retorna uma lista vazia
        if not appointments:
            return jsonify([]), 200

        # Monta a resposta
        response = []
        for ap in appointments:
            charger = Charger.query.get(ap.charger_id)
            location = Location.query.get(charger.location_id) if charger else None

            response.append({
                "id": ap.id,
                "local": location.name if location else "Desconhecido",
                "endereco": location.address if location else "Desconhecido",
                "start_time": ap.start_time.isoformat(),
                "end_time": ap.end_time.isoformat(),
                "status": ap.status
            })

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@appointment_bp.route("/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    """
    Exclui um agendamento pelo ID
    ---
    tags:
      - Agendamentos
    parameters:
      - name: appointment_id
        in: path
        type: integer
        required: true
        description: ID do agendamento a ser excluído
        example: 5
    responses:
      200:
        description: Agendamento excluído com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: Agendamento excluído com sucesso
      404:
        description: Agendamento não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Agendamento não encontrado
      500:
        description: Erro interno no servidor
        schema:
          type: object
          properties:
            error:
              type: string
              example: Erro inesperado ao tentar excluir o agendamento
    """
    try:
        # Buscar o agendamento pelo ID
        appointment = Appointment.query.get(appointment_id)

        # Se o agendamento não existir, retorna erro
        if not appointment:
            return jsonify({"error": "Agendamento não encontrado"}), 404

        # Remover o agendamento do banco de dados
        db.session.delete(appointment)
        db.session.commit()

        return jsonify({"message": "Agendamento excluído com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500