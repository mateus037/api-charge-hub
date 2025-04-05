from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models import db
from models.user import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    """
    Cria um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: João da Silva
            email:
              type: string
              example: joao@email.com
            password:
              type: string
              example: senha123
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
            id:
              type: integer
            name:
              type: string
            email:
              type: string
    """
    data = request.json
    
    # Gerar o hash da senha
    hashed_password = generate_password_hash(data['password'])
    
    # Criar o novo usuário
    new_user = User(name=data['name'], email=data['email'], password_hash=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'Usuário criado com sucesso!',
        'id': new_user.id,  # Agora retornamos o ID
        'name': new_user.name,
        'email': new_user.email
    }), 201
    
@user_bp.route('/login', methods=['POST'])
def login():
    """
    Realiza login de um usuário
    ---
    tags:
      - Usuários
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: joao@email.com
            password:
              type: string
              example: senha123
    responses:
      200:
        description: Login realizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: João da Silva
            email:
              type: string
              example: joao@email.com
      400:
        description: Email e senha são obrigatórios
        schema:
          type: object
          properties:
            error:
              type: string
              example: Email e senha são obrigatórios!
      401:
        description: Senha incorreta
        schema:
          type: object
          properties:
            error:
              type: string
              example: Senha incorreta
      404:
        description: Usuário não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Usuário não encontrado
    """
    print(request.json)
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Verificar se os dados foram fornecidos
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios!'}), 400

    # Procurar o usuário no banco de dados
    user = User.query.filter_by(email=email).first()

    # Verificar se o usuário existe
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    # Verificar se a senha está correta
    if not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Senha incorreta'}), 401

    # Retornar as propriedades name, email e uma mensagem de sucesso
    return jsonify({
        'id': user.id,  # Adicionamos o ID aqui
        'name': user.name,
        'email': user.email,
    })