# run.py (na raiz do projeto)
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app   # <= aqui

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
