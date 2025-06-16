from database import db
from models.tags import chamado_tags, Tag

class Chamado (db.Model):
    id= db.Column(db.Integer, primary_key=True)
    problema = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    ocorrido = db.Column(db.String(250), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('acesso.id'), nullable=False)

    tags = db.relationship(
        'Tag',
        secondary=chamado_tags,
        back_populates='chamados'
    )

    usuario = db.relationship('Usuario', back_populates='chamados')

    def to_dict(self, include_tags=True):
        data = {
            "id": self.id,
            "problema": self.problema,
            "nome": self.nome,
            "email": self.email,
            "numero": self.numero,
            "ocorrido": self.ocorrido,
            "usuario_id": self.usuario_id
        }
    
        if include_tags and hasattr(self, "tags"):
            data["tags"] = [tag.nome for tag in self.tags]
        
        return data
    