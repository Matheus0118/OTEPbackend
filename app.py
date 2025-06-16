from flask import Flask
from flask_cors import CORS
from database import init_app, db
from routes.chamado_routes import chamado_bp
from routes.acesso_routes import acesso_routes
from flask_jwt_extended import JWTManager

from models.chamado import Chamado
from models.tags import Tag

app = Flask(__name__)
CORS(app, resources={r"/*": {
      "origins": ["http://localhost:8081"],
      "methods": ["GET", "POST", "PUT", "DELETE"],
      "allow_headers": ["Content-Type", "Authorization"]
}})

app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta-supersegura'
jwt = JWTManager(app)

init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(acesso_routes)
app.register_blueprint(chamado_bp)
    


if __name__ == '__main__':
        app.run(debug=True)