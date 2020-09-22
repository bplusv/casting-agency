import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from flask_cors import CORS

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.route('/')
def index():
  return 'hello world!'
