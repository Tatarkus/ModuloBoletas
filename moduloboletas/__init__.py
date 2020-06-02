from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from dataclasses import dataclass
from sqlalchemy import extract,func
from datetime import date
import locale
locale.setlocale(locale.LC_ALL, 'es_MX')
import datetime
import calendar

app = Flask(__name__)
app.secret_key = "millavesecreta"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/sonrisadb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    return redirect(url_for('index'))
