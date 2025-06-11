from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_app(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:Mathadm@localhost:5432/OTEPSolucoes_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)