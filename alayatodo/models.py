from flask import Flask, g

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlite3,os

app = Flask(__name__)
app.config.from_object(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir,'/tmp/alayatodo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Todo(db.Model):
    __tablename__ = "todos"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,default=None, nullable=True)
    description=db.Column(db.String,default=None, nullable=True)
    completed=db.Column(db.Integer,default=0,nullable=True)
    def __repr__(self):
	    return 'new to do table is be ini'

class User(db.Model):
    __tablename__ = "users"
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),default=None, nullable=True)
    password=db.Column(db.String(255),default=None, nullable=True)
    
    def __repr__(self):
	   return 'user table'

