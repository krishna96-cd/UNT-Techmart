from flask import Flask
from app import init_db

app = Flask(__name__)

with app.app_context():
    init_db()
