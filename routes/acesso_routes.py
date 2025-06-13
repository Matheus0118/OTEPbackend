from flask import Blueprint, request, jsonify
from models.acesso import Usuario
from database import db
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt
from functools import wraps

acesso_routes = Blueprint('acesso_routes', __name__, url_prefix="/api")

@acesso_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    senha = data.get("senha")

    user = Usuario.query.filter_by(usuario=usuario).first()
    if user and user.verificar_senha(senha):
        access_token = create_access_token(identity=str(user.id), additional_claims={"admin": user.admin})
        return jsonify({"success": True, 
                        "message": "Login realizado com sucesso.", 
                        "token": access_token,
                        "is_admin": user.admin
                        }), 200
    return jsonify({"success": False, "message": "Usuário ou senha inválidos."}), 401

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("admin"):
            return jsonify({"msg": "Acesso restrito a adms."}), 403
        return fn(*args, **kwargs)
    return wrapper

@acesso_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    novo_usuario = Usuario(usuario=data["usuario"])
    novo_usuario.set_senha(data['senha'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"success": True, "message": "Usuário criado com sucesso."})