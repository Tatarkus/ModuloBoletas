from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
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

from moduloboletas.boletas.boletas import boletas_bp
from moduloboletas.reportes.reportes import reportes_bp
app.register_blueprint(boletas_bp,url_prefix='/boletas')
app.register_blueprint(reportes_bp,url_prefix='/reportes')

@app.route('/')
def root():
    return redirect(url_for('boletas.index'))
