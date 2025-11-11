from flask import Flask
from .routes import bp
import os

def create_app():
    app = Flask(__name__)

    # Carregar configurações
    app.config.from_pyfile('../config.py', silent=True)

    # Garantir que a secret_key está setada
    app.secret_key = app.config.get("SECRET_KEY") or os.environ.get("SECRET_KEY") or "chave-super-secreta"

    # Registrar o Blueprint principal
    app.register_blueprint(bp)

    return app
