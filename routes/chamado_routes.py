from flask import Blueprint, jsonify, request
from models.chamado import Chamado
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.acesso_routes import admin_required

chamado_bp = Blueprint('chamado_bp', __name__, url_prefix='/api/chamados')

@chamado_bp.route('/admin/todos', methods=['GET'])
@jwt_required()
@admin_required
def listar_todos_chamados():
    chamados = Chamado.query.all()
    return jsonify([c.to_dict() for c in chamados]), 200

@chamado_bp.route('', methods=['GET'])
@jwt_required()
def listar_chamados():
    usuario_id = get_jwt_identity()
    print("ID do usuário autenticado:", usuario_id)
    chamados = Chamado.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([c.to_dict() for c in chamados])

@chamado_bp.route('', methods=['POST'])
@jwt_required()
def criar_chamado():
    usuario_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Json inválido ou não enviado'}), 400
    chamado = Chamado(
        problema=data.get('problema'),
        nome=data.get('nome'),
        email=data.get('email'),
        numero=data.get('numero'),
        ocorrido=data.get('ocorrido'),
        usuario_id=usuario_id
    )
    db.session.add(chamado)
    db.session.commit()
    return jsonify(chamado.to_dict()), 201

@chamado_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_chamado(id):
    chamado = Chamado.query.get(id)
    if not chamado:
        return jsonify({'error': 'Chamado não encontrado'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON inválido ou não enviado'}), 400

    chamado.problema = data.get('problema', chamado.problema)
    chamado.nome = data.get('nome', chamado.nome)
    chamado.email = data.get('email', chamado.email)
    chamado.numero = data.get('numero', chamado.numero)
    chamado.ocorrido = data.get('ocorrido', chamado.ocorrido)

    db.session.commit()
    return jsonify(chamado.to_dict()), 200

@chamado_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_chamado(id):
    chamado = Chamado.query.get(id)
    if not chamado:
        return jsonify({'error': 'Chamado não encontrado'}), 404
    
    db.session.delete(chamado)
    db.session.commit()
    return jsonify({'message': 'Chamado deletado'}), 200


