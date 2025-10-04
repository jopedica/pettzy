# app/__init__.py
from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)
    # carregar config da raiz (config.py)
    app.config.from_pyfile('../config.py', silent=True)
    # ou: app.config.from_object('config')

    app.register_blueprint(bp)
    return app
