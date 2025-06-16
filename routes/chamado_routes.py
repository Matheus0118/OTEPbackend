from flask import Blueprint, jsonify, request
from models.chamado import Chamado
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.acesso_routes import admin_required
from models.tags import Tag


chamado_bp = Blueprint('chamado_bp', __name__, url_prefix='/api/chamados')

@chamado_bp.route('/admin/todos', methods=['GET'])
@jwt_required()
@admin_required
def listar_todos_chamados():
    chamados = Chamado.query.all()
    return jsonify([c.to_dict(include_tags=True) for c in chamados]), 200

@chamado_bp.route('', methods=['GET'])
@jwt_required()
def listar_chamados():
    usuario_id = get_jwt_identity()
    print("ID do usuário autenticado:", usuario_id)
    chamados = Chamado.query.filter_by(usuario_id=usuario_id).all()
    lista_chamados = [c.to_dict(include_tags=False) for c in chamados]
    print("Lista de chamados:", lista_chamados)
    return jsonify(lista_chamados)

@chamado_bp.route('', methods=['POST'])
@jwt_required()
def criar_chamado():
    usuario_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Json inválido ou não enviado'}), 400
    
    campos_obrigatorios = [ 'problema', 'nome', 'email', 'numero', 'ocorrido']
    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({'error': f'Campo obrigatório "{campo}" ausente ou vazio'}), 400
            
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

@chamado_bp.route('/<int:id>/tags', methods=['PUT'])
@jwt_required()
@admin_required
def atualizar_tags(id):
    chamado = Chamado.query.get(id)
    if not chamado:
        return jsonify({"error": "Chamado não encontrado"}), 404

    data = request.get_json()
    tag_nomes = data.get("tags", [])

    tags = []
    for nome in tag_nomes:
        tag = Tag.query.filter_by(nome=nome).first()
        if not tag:
            tag = Tag(nome=nome)
            db.session.add(tag)
        tags.append(tag)

    chamado.tags = tags
    db.session.commit()
    return jsonify(chamado.to_dict()), 200


