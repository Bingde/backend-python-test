from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlite3
import os
# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

file_path = "/tmp/alayatodo.db"

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app,db)
from alayatodo import models

class ExampleTable(db.Model):
	__tablename__ ='ExampleTable'
	id = db.Column(db.Integer,primary_key=True)

# class Todo(db.Model):
#     __tablename__ = "todos"
#  
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer,default=None, nullable=True)
#     description=db.Column(db.String,default=None, nullable=True)
#     completed=db.Column(db.Integer,default=0,nullable=True)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn
    
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
        
import alayatodo.views