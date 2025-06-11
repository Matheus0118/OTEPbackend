from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__= 'acesso'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(512), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    chamados = db.relationship('Chamado', back_populates='usuario', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
            return check_password_hash(self.senha_hash, senha) 
    