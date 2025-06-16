from database import db

chamado_tags = db.Table(
    'chamado_tags',
    db.Column('chamado_id', db.Integer, db.ForeignKey('chamado.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__='tag'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    chamados = db.relationship(
        'Chamado',
        secondary=chamado_tags,
        back_populates='tags'
    )