# config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")  # FIXO!
    # sessão (cookies)
    SESSION_COOKIE_NAME = "pettzy_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False     # True só com HTTPS
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


    # Configurações de banco de dados MySQL
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASS = os.environ.get("DB_PASS", "Thor2804!")
    DB_NAME = os.environ.get("DB_NAME", "pettzy")
