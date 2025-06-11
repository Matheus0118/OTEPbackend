from database import db

class Chamado (db.Model):
    id= db.Column(db.Integer, primary_key=True)
    problema = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    ocorrido = db.Column(db.String(250), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('acesso.id'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='chamados')

    def to_dict(self):
        return {
            "id": self.id,
            "problema": self.problema,
            "nome": self.nome,
            "email": self.email,
            "numero": self.numero,
            "ocorrido": self.ocorrido,
            "usuario_id": self.usuario_id
        }
    
    